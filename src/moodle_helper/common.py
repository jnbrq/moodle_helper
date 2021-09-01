from jinja2 import Template

def template(f):
    def closure(self, *args, **kwargs):
        r = f(self, *args, **kwargs)
        if r is None:
            return "@@NONE@@"
        template = Template(r)
        return template.render(q=self)
    return closure
