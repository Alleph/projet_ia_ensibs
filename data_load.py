from lxml import etree

root = etree.parse(r'TRAIN_ENSIBS\TestbedSatJun12Flows.xml')
# Print the loaded XML

for child in root:
    print(child.tag)