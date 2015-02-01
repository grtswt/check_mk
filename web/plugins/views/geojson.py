#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# Mostly stolen from check_mk

json_escape = re.compile(r'[\\"\r\n\t\b\f\x00-\x1f]')
json_encoding_table = dict([(chr(i), '\\u%04x' % i) for i in range(32)])
json_encoding_table.update({'\b': '\\b', '\f': '\\f', '\n': '\\n', '\r': '\\r', '\t': '\\t', '\\': '\\\\', '"': '\\"' })

def encode_string_json(s):
    return '"' + json_escape.sub(lambda m: json_encoding_table[m.group(0)], s) + '"'

def render_geojson(rows, view, group_painters, painters, num_columns, show_checkboxes, export = False):
    sitename = rows[0]["site"]
    site = html.site_status[sitename]["site"]
    if export:
        html.req.content_type = "appliation/json; charset=UTF-8"
        filename = 'GeoJSON_%s-%s.json' % (view['name'], time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))
        html.req.headers_out['Content-Disposition'] = 'Attachment; filename=%s' % filename

    html.write('{\n  "type": "FeatureCollection",\n    "features": [\n')
    first = True
    for row in rows:
        custom_vars = dict(zip(row["host_custom_variable_names"],row["host_custom_variable_values"]))
        if  "POSITION" in custom_vars and custom_vars.get("POSITION") != "":
            link = "view.py?view_name=host&host=%s" % html.urlencode(row["host_name"])
            if first:
                first = False
            else:
                html.write(",\n")

            html.write('    {\n')
            html.write('      "type": "Feature",\n')
            html.write('      "id": "%s",\n' % row["host_name"])
            html.write('      "geometry": {\n')
            html.write('        "type": "Point",\n')
            html.write('        "coordinates": [%s]\n' % custom_vars.get("POSITION"))
            html.write('      },')
            html.write('      "properties": {\n')
            html.write('        "href": "%s",\n' % link)
            html.write('        "state": "%s",\n' % row["host_state"])
            html.write('        "hostname": "%s",\n' % row["host_name"])
            html.write('        "s_crit": "%s",\n' % row["host_num_services_crit"])
            html.write('        "s_warn": "%s",\n' % row["host_num_services_warn"])
            html.write('        "s_ok": "%s",\n'   % row["host_num_services_ok"])
            html.write('        "s_pending": "%s",\n' % row["host_num_services_pending"])
            html.write('        "s_unknown": "%s"\n' % row["host_num_services_unknown"])
            #html.write('        "address": "%s"\n' % row["host_address"])
            #html.write('        "alias": "%s"\n' % row["host_alias"])
            html.write('      }\n')
            html.write('    }')

    html.write("\n  ]\n}\n")


multisite_layouts["geojson_export"] = {
    "title"  : _("GeoJSON data export"),
    "render" : lambda a,b,c,d,e,f: render_geojson(a,b,c,d,e,f,True),
    "group"  : False,
    "hide"   : True,
}

multisite_layouts["geojson"] = {
    "title"  : _("GeoJSON data output"),
    "render" : lambda a,b,c,d,e,f: render_geojson(a,b,c,d,e,f,False),
    "group"  : False,
    "hide"   : True,
}
