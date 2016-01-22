# Written by Gem Newman. This work is licensed under a Creative Commons         
# Attribution-ShareAlike 4.0 International License.                    


from quote import app, controller


@app.route('/<root>/<output>')
@app.route('/<root>', defaults={'output': 'html'})
@app.route('/', defaults={'root':app.config['DEFAULT_ROOT'], 'output':'html'})
def index(root, output):
    return controller.get(root, output)
