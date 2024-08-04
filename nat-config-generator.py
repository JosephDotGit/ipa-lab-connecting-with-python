from jinja2 import Environment, FileSystemLoader
import yaml

loader = FileSystemLoader("templates")
env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
template = env.get_template("router-nat.j2")
with open("data/routers-nat.yml", 'r') as f:
    routers = yaml.safe_load(f)
with open("config/R2-exercise-nat.txt", 'w') as f:
    f.write(template.render(routers))