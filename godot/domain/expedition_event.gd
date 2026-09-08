class_name ExpeditionEventModel
extends RefCounted

const CanonicalData = preload("res://autoload/canonical_data.gd")

var _events: Array[Dictionary] = []
var _load_error := ""


func _init() -> void:
    var loader := CanonicalData.new()
    var result := loader.read_csv(
        "data/expedition_events.csv",
        [
            "event_id",
            "expedition_id",
            "sequence",
            "trajectory_id",
            "subject_type",
            "subject_label",
            "event_type",
            "origin_node",
            "destination_node",
            "date_from",
            "date_to",
            "date_precision",
            "variant_group",
            "preferred_for_simulation",
            "evidence_grade",
            "evidence_scope",
            "source_id",
            "notes",
        ]
    )
    if not bool(result.get("ok", false)):
        _load_error = String(result.get("error", "Falha ao carregar expedition_events.csv"))
        return

    for row in result.get("rows", []):
        var event := _normalize(row)
        _events.append(event)
    _events.sort_custom(_event_before)


func is_ready() -> bool:
    return _load_error.is_empty()


func load_error() -> String:
    return _load_error


func for_expedition(expedition_id: String) -> Array[Dictionary]:
    var selected: Array[Dictionary] = []
    for event in _events:
        if String(event.get("expedition_id", "")) == expedition_id:
            selected.append(event.duplicate(true))
    return selected


func preferred_for_expedition(expedition_id: String) -> Array[Dictionary]:
    var selected: Array[Dictionary] = []
    for event in for_expedition(expedition_id):
        if bool(event.get("preferred_for_simulation", false)):
            selected.append(event)
    return selected


func available_by(expedition_id: String, on_date: String) -> Array[Dictionary]:
    var selected: Array[Dictionary] = []
    for event in for_expedition(expedition_id):
        if String(event.get("date_to", "")) <= on_date:
            selected.append(event)
    return selected


func _normalize(row: Dictionary) -> Dictionary:
    var date_from := String(row.get("date_from", ""))
    var date_to := String(row.get("date_to", ""))
    if date_to.is_empty():
        date_to = date_from

    return {
        "event_id": String(row.get("event_id", "")),
        "expedition_id": String(row.get("expedition_id", "")),
        "sequence": int(String(row.get("sequence", "0"))),
        "trajectory_id": String(row.get("trajectory_id", "")),
        "subject_type": String(row.get("subject_type", "")),
        "subject_label": String(row.get("subject_label", "")),
        "event_type": String(row.get("event_type", "")),
        "origin_node": _nullable_string(row.get("origin_node", "")),
        "destination_node": _nullable_string(row.get("destination_node", "")),
        "date_from": date_from,
        "date_to": date_to,
        "date_precision": String(row.get("date_precision", "")),
        "variant_group": _nullable_string(row.get("variant_group", "")),
        "preferred_for_simulation": String(row.get("preferred_for_simulation", "")) == "TRUE",
        "evidence_grade": String(row.get("evidence_grade", "")),
        "evidence_scope": String(row.get("evidence_scope", "")),
        "source_id": String(row.get("source_id", "")),
        "notes": String(row.get("notes", "")),
    }


func _nullable_string(value: Variant) -> Variant:
    var text := String(value)
    return null if text.is_empty() else text


func _event_before(a: Dictionary, b: Dictionary) -> bool:
    var a_expedition := String(a.get("expedition_id", ""))
    var b_expedition := String(b.get("expedition_id", ""))
    if a_expedition != b_expedition:
        return a_expedition < b_expedition
    var a_sequence := int(a.get("sequence", 0))
    var b_sequence := int(b.get("sequence", 0))
    if a_sequence != b_sequence:
        return a_sequence < b_sequence
    return String(a.get("event_id", "")) < String(b.get("event_id", ""))
