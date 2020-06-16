import json

with open('src/endpoint_mapping.json') as f:
    endpoints = json.load(f)

with open('docs/endpoint_parameters.md', 'w') as f:
    for endpoint in endpoints:
        line = '## {} \n'.format(endpoint)
        f.write(line)

        header_line = '| Parameter | CREATE required | UPDATE required | ReadOnly |DataType | Description |\n'
        f.write(header_line)
        sub_header_line = '|-|-|-|-|-|-|\n'
        f.write(sub_header_line)

        for i in endpoints[endpoint]['attributes']:
            line = '| {} | {} | {} | {} | {} | {} |\n'.format(
                i,
                True if i in endpoints[endpoint]['create_required'] else '',
                True if i in endpoints[endpoint]['update_required'] else '',
                True if 'read_only' in endpoints[endpoint]['attributes'][i] else '',
                endpoints[endpoint]['attributes'][i]['type'],
                endpoints[endpoint]['attributes'][i]['description']
            )
            f.write(line)

        f.write('\n')
