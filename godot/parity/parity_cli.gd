extends SceneTree

const CanonicalData = preload("res://autoload/canonical_data.gd")
const NodeStateModel = preload("res://domain/node_state.gd")
const ExpeditionEventModel = preload("res://domain/expedition_event.gd")


func _initialize() -> void:
    var loader := CanonicalData.new()
    if not _canonical_data_smoke(loader):
        quit(1)
        return

    if not _node_state_parity():
        quit(1)
        return

    if not _expedition_event_parity():
        quit(1)
        return

    quit(0)


func _canonical_data_smoke(loader: CanonicalData) -> bool:
    var required_headers: Array[String] = [
        "event_id",
        "node_id",
        "date_from",
        "date_to",
        "date_precision",
        "event_type",
        "institutional_presence",
        "fortification_state",
        "garrison_state",
        "access_state",
        "relationship_state",
        "sovereignty_note",
    ]
    var result := loader.read_csv("data/node_state_events.csv", required_headers)
    if not bool(result.get("ok", false)):
        push_error(String(result.get("error", "Falha desconhecida ao ler dados canônicos")))
        return false

    var rows: Array = result.get("rows", [])
    var f5_event_count := 0
    for row in rows:
        var event_id := String(row.get("event_id", ""))
        if event_id.contains("1505"):
            f5_event_count += 1

    var payload := {
        "status": "ok",
        "engine": Engine.get_version_info().get("string", "unknown"),
        "canonical_file": "data/node_state_events.csv",
        "row_count": rows.size(),
        "f5_event_count": f5_event_count,
        "repository_root": loader.repository_root(),
    }
    print("PARITY_SMOKE=" + JSON.stringify(payload))
    return true


func _node_state_parity() -> bool:
    var model := NodeStateModel.new()
    if not model.is_ready():
        push_error(model.load_error())
        return false

    var fixture_file := FileAccess.open(
        "res://parity/fixtures/node_state_1505_12_31.json",
        FileAccess.READ
    )
    if fixture_file == null:
        push_error("Fixture de golden state indisponível")
        return false

    var fixture = JSON.parse_string(fixture_file.get_as_text())
    if typeof(fixture) != TYPE_DICTIONARY:
        push_error("Fixture de golden state não é um objeto JSON")
        return false

    var freeze_date := String(fixture.get("freeze_date", ""))
    var expected_nodes: Dictionary = fixture.get("nodes", {})
    var node_ids := expected_nodes.keys()
    node_ids.sort()

    for node_id_variant in node_ids:
        var node_id := String(node_id_variant)
        var actual := model.effective_state(node_id, freeze_date)
        var expected: Dictionary = expected_nodes[node_id]
        if actual != expected:
            push_error(
                "Paridade NodeState falhou em %s\nexpected=%s\nactual=%s" % [
                    node_id,
                    JSON.stringify(expected),
                    JSON.stringify(actual),
                ]
            )
            return false

    # Gate temporal conservador: RANGE não pode antecipar o limite superior.
    var can_before := model.effective_state("CAN", "1505-10-30")
    var can_after := model.effective_state("CAN", "1505-10-31")
    if String(can_before.get("fortification_state", "")) == "PORTUGUESE_FORT":
        push_error("CAN1505_E01 foi aplicado antes do limite superior")
        return false
    if String(can_after.get("fortification_state", "")) != "PORTUGUESE_FORT":
        push_error("CAN1505_E01 não foi aplicado no limite superior")
        return false

    var anj_before := model.effective_state("ANJ", "1505-09-29")
    var anj_after := model.effective_state("ANJ", "1505-09-30")
    if String(anj_before.get("fortification_state", "")) == "PORTUGUESE_FORT":
        push_error("ANJ1505_E01 foi aplicado antes do limite superior")
        return false
    if String(anj_after.get("fortification_state", "")) != "PORTUGUESE_FORT":
        push_error("ANJ1505_E01 não foi aplicado no limite superior")
        return false

    var payload := {
        "status": "ok",
        "contract": "NodeStateEventModel",
        "freeze_date": freeze_date,
        "nodes": node_ids,
        "range_boundaries": ["ANJ1505_E01", "CAN1505_E01"],
    }
    print("NODE_STATE_PARITY=" + JSON.stringify(payload))
    return true


func _expedition_event_parity() -> bool:
    var model := ExpeditionEventModel.new()
    if not model.is_ready():
        push_error(model.load_error())
        return false

    var fixture_file := FileAccess.open(
        "res://parity/fixtures/almeida_1505_expedition_events.json",
        FileAccess.READ
    )
    if fixture_file == null:
        push_error("Fixture de ExpeditionEvent indisponível")
        return false

    var fixture = JSON.parse_string(fixture_file.get_as_text())
    if typeof(fixture) != TYPE_DICTIONARY:
        push_error("Fixture de ExpeditionEvent não é um objeto JSON")
        return false

    var expedition_id := String(fixture.get("expedition_id", ""))
    var events := model.for_expedition(expedition_id)
    var ordered_ids := _event_ids(events)
    var expected_order: Array = fixture.get("ordered_event_ids", [])
    if ordered_ids != expected_order:
        push_error(
            "Ordenação ExpeditionEvent divergiu\nexpected=%s\nactual=%s" % [
                JSON.stringify(expected_order),
                JSON.stringify(ordered_ids),
            ]
        )
        return false

    var availability: Dictionary = fixture.get("availability", {})
    var dates := availability.keys()
    dates.sort()
    for date_variant in dates:
        var on_date := String(date_variant)
        var actual_ids := _event_ids(model.available_by(expedition_id, on_date))
        var expected_ids: Array = availability[on_date]
        if actual_ids != expected_ids:
            push_error(
                "Disponibilidade ExpeditionEvent divergiu em %s\nexpected=%s\nactual=%s" % [
                    on_date,
                    JSON.stringify(expected_ids),
                    JSON.stringify(actual_ids),
                ]
            )
            return false

    var by_id: Dictionary = {}
    for event in events:
        by_id[String(event.get("event_id", ""))] = event

    var selected_fields: Dictionary = fixture.get("selected_fields", {})
    for event_id_variant in selected_fields.keys():
        var event_id := String(event_id_variant)
        if not by_id.has(event_id):
            push_error("Evento esperado ausente: %s" % event_id)
            return false
        var actual_event: Dictionary = by_id[event_id]
        var expected_fields: Dictionary = selected_fields[event_id]
        for field_variant in expected_fields.keys():
            var field := String(field_variant)
            if actual_event.get(field) != expected_fields[field]:
                push_error(
                    "Campo ExpeditionEvent divergiu em %s.%s: expected=%s actual=%s" % [
                        event_id,
                        field,
                        JSON.stringify(expected_fields[field]),
                        JSON.stringify(actual_event.get(field)),
                    ]
                )
                return false

    var payload := {
        "status": "ok",
        "contract": "ExpeditionEventModel",
        "expedition_id": expedition_id,
        "ordered_event_ids": ordered_ids,
        "availability_checkpoints": dates,
    }
    print("EXPEDITION_EVENT_PARITY=" + JSON.stringify(payload))
    return true


func _event_ids(events: Array[Dictionary]) -> Array:
    var ids: Array = []
    for event in events:
        ids.append(String(event.get("event_id", "")))
    return ids
