from datetime import timedelta 

def format_date(start, end):
    if not end - start > timedelta(days=1):
      return str(start.strftime('%A, %B %d, %Y')) + ' From ' + str(start.strftime('%I:%M %p')) + ' To ' + str(end.strftime('%I:%M %p')) 

    return str(start.strftime('%A, %B %d, %Y. %I:%M %p')) + ' - ' + str(end.strftime('%A, %B %d, %Y. %I:%M %p'))
