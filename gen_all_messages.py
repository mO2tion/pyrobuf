import glob
import re

from jinja2 import Environment, PackageLoader

from parse_proto import Parser

def gen_all_messages():
    get_name = re.compile(r'([A-Za-z][A-Za-z0-9_]*).proto').match
    parser = Parser()

    env = Environment(loader=PackageLoader('protobuf', 'templates'))

    for spec in glob.glob('messages/*.proto'):
        print("parsing %s" % spec)

        m = get_name(spec[spec.rfind('/')+1:])
        name_pxd = "%s_proto.pxd" % m.group(1)
        name_pyx = "%s_proto.pyx" % m.group(1)

        msgdef = parser.parse_from_filename(spec)

        templ_pxd = env.get_template('proto_pxd.tmpl')
        templ_pyx = env.get_template('proto_pyx.tmpl')

        with open('out/' + name_pxd, 'w') as fp:
            fp.write(templ_pxd.render(msgdef))

        with open('out/' + name_pyx, 'w') as fp:
            fp.write(templ_pyx.render(msgdef))

if __name__ == "__main__":
    gen_all_messages()
