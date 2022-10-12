import re

# IDs = re.sub("[v=]", "", "https://www.youtube.com/watch?v=mTHMLl4dQpw", 1)
url = "https://www.youtube.com/watch?v=mTHMLl4dQpw"
IDs = url.find("v=") + 2
IDs = url[IDs:]
ytb = "https://youtu.be/"
newlink =  ytb + IDs
newlink = newlink + "?" + "start=" + str(0) + "&" + "end=" + str(60)

print(newlink)