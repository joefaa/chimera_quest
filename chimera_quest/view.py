import jinja2
from chimera_quest.model import chimera_quest
import cgi

def application( environ, start_response ):
    # This line tells the template loader where to search for template files
    templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )

    # This creates your environment and loads a specific template
    env = jinja2.Environment( loader=templateLoader )
    template = env.get_template( 'main.html' )
    template = template.render()
    start_response("200 OK", [( "Content-Type", "text/html" )])
    yield(template.encode( "utf8" ))
    # tissue_type = None
    # input_type = None
    #
    # if environ['REQUEST_METHOD'] == 'POST':
    #     post_env = environ.copy()
    #     post_env['QUERY_STRING'] = ''
    #     post = cgi.FieldStorage(
    #         fp=environ['wsgi.input'],
    #         environ=post_env,
    #         keep_blank_values=True
    #     )
    #     # get values
    #     input_type = post.getvalue( 'input_type' )
    #     tissue_type = post.getvalue( 'tissue_type')
    #
    #
    # start_response("200 OK", [( "Content-Type", "text/html" )])
    #
    # if input_type:
    #     fusion_list = chimera_quest()
    #     template = template.render( fusion_list = fusion_list )
    #     yield(template.encode( "utf8" ))
    # else:
    #     template = template.render()
    #     yield(template.encode( "utf8" ))
