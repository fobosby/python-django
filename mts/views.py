from django.shortcuts import render_to_response
from mts.charts import BarChart, AngularChart
from mts.forms import LoadXMLForm
from mts.models import DataRecord, OUTGOING
from mts.utilites import file_handler


def load_file(request):
    if request.method == 'POST':
        form = LoadXMLForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            result = file_handler(request.FILES['xml'])
            return render_to_response("mts/LoadFile.html", {'passed': u'File load successfully', 'result': result})
        else:
            return render_to_response("mts/LoadFile.html", {'form': form})
    return render_to_response("mts/LoadFile.html", {'form': LoadXMLForm()})


COUNT = 25


def calls_analyze(request):
    time_chart = BarChart(DataRecord.get_top_calls_info(COUNT, 'time', direction=OUTGOING),
                       title='Top %s outgoing callers' % COUNT,
                       y_axis_label='Summary calls time (seconds)',
                       color='orange').to_json()

    call_count_chart = BarChart(DataRecord.get_top_calls_info(COUNT, 'count', direction=OUTGOING),
                             title='Calls count for top %s outgoing callers' % COUNT,
                             y_axis_label='Total outgoing calls (count)').to_json()

    call_avg_chart = BarChart(DataRecord.get_top_calls_info(COUNT, 'average_time', direction=OUTGOING),
                           title='Average call time for top %s outgoing callers' % COUNT,
                           y_axis_label='Average time (seconds)',
                           color='green').to_json()

    velcom_summary = AngularChart(DataRecord.get_call_volume(direction=OUTGOING, operator_name='Velcom'), title='Outgoing Velcom Calls', axis_label='%').to_json()
    mts_summary = AngularChart(DataRecord.get_call_volume(direction=OUTGOING, operator_name='MTS'), title='Outgoing MTS Calls', axis_label='%').to_json()
    return render_to_response("mts/Analitycs.html", {'time_chart': time_chart,
                                                       'call_count_chart': call_count_chart,
                                                       'call_avg_chart': call_avg_chart,
                                                       'velcom_summary': velcom_summary,
                                                       'mts_summary': mts_summary})

