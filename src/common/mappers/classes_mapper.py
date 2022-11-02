import datetime as dt

def break_class_into_events(class_obj):
    event_list = []

    if isinstance(class_obj['start_time'], list):
        for i in range(len(class_obj['start_time'])):
            event = class_obj.copy()
            event['start_time'] = dt.datetime.strptime(class_obj['start_time'][i], '%H:%M').time()
            event['end_time'] = dt.datetime.strptime(class_obj['end_time'][i], '%H:%M').time()
            event['week_days'] = class_obj['week_days'][i]
            # import pdb; pdb.set_trace()
            if len(class_obj['professors']) > i:
                event['professors'] = class_obj['professors'][i]

            event['event_id'] = str(event['subject_code']) + '_' + str(event['class_code']) + '_' + str(i)
            event['class_id'] = str(event['subject_code']) + '_' + str(event['class_code'])


            event_list.append(event)

    return event_list