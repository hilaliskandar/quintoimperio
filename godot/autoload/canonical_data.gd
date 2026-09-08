class_name CanonicalData
extends RefCounted


func repository_root() -> String:
    var project_root := ProjectSettings.globalize_path("res://").trim_suffix("/")
    return project_root.get_base_dir().simplify_path()


func canonical_path(relative_path: String) -> String:
    return repository_root().path_join(relative_path).simplify_path()


func read_csv(relative_path: String, required_headers: Array[String] = []) -> Dictionary:
    var path := canonical_path(relative_path)
    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        return {
            "ok": false,
            "error": "CSV canônico indisponível: %s" % path,
            "path": path,
            "headers": [],
            "rows": [],
        }

    if file.eof_reached():
        return {
            "ok": false,
            "error": "CSV canônico vazio: %s" % path,
            "path": path,
            "headers": [],
            "rows": [],
        }

    var header_values := file.get_csv_line(",")
    var headers: Array[String] = []
    for value in header_values:
        headers.append(String(value))

    for required_header in required_headers:
        if not headers.has(required_header):
            return {
                "ok": false,
                "error": "Cabeçalho obrigatório ausente em %s: %s" % [relative_path, required_header],
                "path": path,
                "headers": headers,
                "rows": [],
            }

    var rows: Array[Dictionary] = []
    while not file.eof_reached():
        var values := file.get_csv_line(",")
        if values.size() == 1 and String(values[0]).is_empty():
            continue
        if values.size() != headers.size():
            return {
                "ok": false,
                "error": "Linha CSV com %d campos; esperados %d em %s" % [values.size(), headers.size(), relative_path],
                "path": path,
                "headers": headers,
                "rows": rows,
            }

        var row: Dictionary = {}
        for index in range(headers.size()):
            row[headers[index]] = String(values[index])
        rows.append(row)

    return {
        "ok": true,
        "error": "",
        "path": path,
        "headers": headers,
        "rows": rows,
    }
