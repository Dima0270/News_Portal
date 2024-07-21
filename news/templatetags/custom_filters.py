from django import template


register = template.Library()


@register.filter()
def censor(value):
   try:
      if type(value) is str:
         value = value.split()
         t = ""
         for i in value:
            if i.lower() in ["цензура", "цензура1", "цензура2", "цензура3", "цензура4"]:
               i = f"{i[:1]}{'*' * (len(i) - 1)}"
            t += f" {i}"
         return t.strip()
      else:
         raise TypeError()
   except TypeError:
      print("Неправильно выбран тип данных")


