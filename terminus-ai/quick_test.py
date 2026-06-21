from ai.parser import AIParser

p = AIParser()
for cmd in ["check mail", "list mail", "check last mail", "show my meetings"]:
    r = p.parse(cmd)
    print(f"{cmd:20} -> {r['service']:10} {r['action']:15} conf={r['confidence']}")
