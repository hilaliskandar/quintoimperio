class_name NodeStateModel
extends RefCounted

const CanonicalData = preload("res://autoload/canonical_data.gd")

var _nodes: Dictionary = {}
var _events: Array[Dictionary] = []
var _load_error := ""


func _init() -> void:
    var loader := CanonicalData.new()
    var nodes_result := loader.read_csv(
        "data/nodes.csv",
        ["node_id", "polity_1497", "access_regime", "fortification"]
    )
    if not bool(nodes_result.get("ok", false)):
        _load_error = String(nodes_result.get("error", "Falha ao carregar nodes.csv"))
        return

    for row in nodes_result.get("rows", []):
        _nodes[String(row.get("node_id", ""))] = row

    var events_result := loader.read_csv(
        "data/node_state_events.csv",
        [
            "event_id",
            "node_id",
            "date_from",
            "date_to",
            "date_precision",
            "institutional_presence",
            "fortification_state",
            "garrison_state",
            "access_state",
            "relationship_state",
            "sovereignty_note",
        ]
    )
    if not bool(events_result.get("ok", false)):
        _load_error = String(events_result.get("error", "Falha ao carregar node_state_events.csv"))
        return

    for row in events_result.get("rows", []):
        var event: Dictionary = row.duplicate(true)
        if String(event.get("date_to", "")).is_empty():
            event["date_to"] = String(event.get("date_from", ""))
        _events.append(event)
    _events.sort_custom(_event_before)


func is_ready() -> bool:
    return _load_error.is_empty()


func load_error() -> String:
    return _load_error


func baseline(node_id: String) -> Dictionary:
    if not _nodes.has(node_id):
        return {"ok": false, "error": "Nó desconhecido: %s" % node_id}

    var node: Dictionary = _nodes[node_id]
    var fortification := String(node.get("fortification", ""))
    if fortification.is_empty():
        fortification = "UNKNOWN"
    var access := String(node.get("access_regime", ""))
    if access.is_empty():
        access = "UNKNOWN"

    return {
        "ok": true,
        "node_id": node_id,
        "institutional_presence": "NONE",
        "fortification_state": fortification,
        "garrison_state": "NONE",
        "access_state": access,
        "relationship_state": "UNESTABLISHED",
        "sovereignty_note": String(node.get("polity_1497", "")),
        "applied_event_ids": [],
    }


func effective_state(node_id: String, on_date: String) -> Dictionary:
    var state := baseline(node_id)
    if not bool(state.get("ok", false)):
        return state

    var applied: Array[String] = []
    for event in _events:
        if String(event.get("node_id", "")) != node_id:
            continue
        # ISO YYYY-MM-DD is lexicographically ordered. The upper bound is
        # deliberate: RANGE events become safely effective only at date_to.
        if on_date < String(event.get("date_to", "")):
            continue

        _apply_nonempty(state, "institutional_presence", event)
        _apply_nonempty(state, "fortification_state", event)
        _apply_nonempty(state, "garrison_state", event)
        _apply_nonempty(state, "access_state", event)
        _apply_nonempty(state, "relationship_state", event)
        _apply_nonempty(state, "sovereignty_note", event)
        applied.append(String(event.get("event_id", "")))

    state["applied_event_ids"] = applied
    return state


func _apply_nonempty(state: Dictionary, key: String, event: Dictionary) -> void:
    var value := String(event.get(key, ""))
    if not value.is_empty():
        state[key] = value


func _event_before(a: Dictionary, b: Dictionary) -> bool:
    var a_date := String(a.get("date_to", ""))
    var b_date := String(b.get("date_to", ""))
    if a_date == b_date:
        return String(a.get("event_id", "")) < String(b.get("event_id", ""))
    return a_date < b_date
