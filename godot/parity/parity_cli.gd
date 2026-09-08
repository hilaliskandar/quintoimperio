extends SceneTree

const CanonicalData = preload("res://autoload/canonical_data.gd")


func _initialize() -> void:
    var loader := CanonicalData.new()
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
        quit(1)
        return

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
    quit(0)
