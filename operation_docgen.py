import assembly_simulator
import inspect
import re


def parse_doc(cmd):
    doc = inspect.getdoc(cmd)
    if not doc:
        return None
    ret = {
        "args": {},
        "description": "",
        "example": []
    }
    desc = True
    example = -1
    for line in doc.split("\n"):
        m = re.match("^:param (\w+):(.*)$", line)
        if m:
            ret["args"][m.group(1)] = m.group(2).strip()
            desc = False
        elif desc:
            ret["description"] += "\n" + line
        m = re.match("^:example:$", line)
        if m:
            example += 1
            ret["example"].append("")
        elif example > -1:
            ret["example"][example] += "\n" + line
            desc = False

    for i in range(len(ret["example"]) - 1):
        if len(ret["example"][i]) == 0:
            del ret["example"][i]
    return ret


def get_args(cmd):
    args = inspect.getargspec(cmd)
    doc = parse_doc(cmd)
    ret = []
    for arg in args[0]:
        ret.append((arg, "" if not doc or not doc["args"] or arg not in doc["args"] else doc["args"][arg]))
    return ret

fout = open("operations.md", "w")
fout.write("#Operations\n")
for cmd in sorted(assembly_simulator.pretty_commands.items(), key=lambda v: v[0]):
    doc = parse_doc(cmd[1])
    args = get_args(cmd[1])
    fout.write("##" + cmd[0] + "\n")
    fout.write("`" + cmd[0] + " " + ", ".join(a[0] for a in args) + "`\n\n")
    fout.write("" if doc is None or len(doc["description"]) == 0 else doc["description"] + "\n")
    for arg in args:
        fout.write("`%s` - %s\n\n" % arg)
    if doc is not None and doc["example"]:
        fout.write("Examples:\n\n")
        for ex in doc["example"]:
            fout.write("```" + ex + "\n")
            fout.write("```\n\n")
fout.close()