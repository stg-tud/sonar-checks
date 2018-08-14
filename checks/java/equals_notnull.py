# check: https://rules.sonarsource.c../../java/RSPEC-4454
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/equals_notnull.java").uast
eq_methods = bblfsh.filter(uast, "//MethodDeclaration/Identifier[@Name='equals']/parent::MethodDeclaration")

for m in eq_methods:
    for c in m.children:
        if c.properties["internalRole"] == 'parameters':
            ann = bblfsh.filter(c, '//MarkerAnnotation//Identifier')
            ann_qualified = '.'.join([i.properties["Name"] for i in ann])

            if ann_qualified == "javax.annotation.Nonnull":
                print("Don't use Nonnull annotation on equals methods, line {}"
                        .format(c.start_position.line))