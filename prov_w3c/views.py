# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
import json
from django.http import JsonResponse
from django.db.models.fields.related import ManyToManyField
from django.core import serializers
from rest_framework.renderers import JSONRenderer
import codecs  # for adding BOM mark at beginning of responses (e.g. json with umlauts)

from .models import Activity, Entity, Used, WasGeneratedBy, Agent, WasAssociatedWith, WasAttributedTo


#def index(request):
#    return HttpResponse("Hello, world. You're at the prov_w3c index.")

class IndexView(generic.ListView):
    template_name = 'prov_w3c/index.html'
    context_object_name = 'activity_list'

    def get_queryset(self):
        """Return the activities (at most 1000, ordered by startTime)."""
        return Activity.objects.order_by('-startTime')[:1000]

class ActivitiesView(generic.ListView):
    template_name = 'prov_w3c/activities.html'
    context_object_name = 'activity_list'

    def get_queryset(self):
        """Return the activities (at most 1000, ordered by startTime)."""
        return Activity.objects.order_by('-startTime')[:1000]


class ActivityDetailView(generic.DetailView):
    model = Activity

    def get_context_data(self, **kwargs):
        context = super(ActivityDetailView, self).get_context_data(**kwargs)
        #context['used_list'] = Used.objects.all()[:]
        #context['wasGeneratedBy_list'] = WasGeneratedBy.objects.all()[:]
        #context['wasAssociatedWith_list'] = WasAssociatedWith.objects.all()[:]
        return context


class EntitiesView(generic.ListView):
    template_name = 'prov_w3c/entities.html'
    context_object_name = 'entity_list'

    def get_queryset(self):
        """Return the entities (at most 1000, ordered by label)."""
        return Entity.objects.order_by('-label')[:1000]


class EntityDetailView(generic.DetailView):
    model = Entity


class AgentsView(generic.ListView):
    template_name = 'prov_w3c/agents.html'
    context_object_name = 'agent_list'

    def get_queryset(self):
        """Return the agents (at most 1000, ordered by label)."""
        return Agent.objects.order_by('-label')[:1000]


class AgentDetailView(generic.DetailView):
    model = Agent


#def graph(request):
#    return render(request, 'prov_w3c/graph.html', {})

def graph(request):
    return render(request, 'prov_w3c/graph.html', {"activity": "mdpl2:act_simulation"})


# serialisations
# simple prov-n view, using just a function:
def provn(request):
    activity_list = Activity.objects.order_by('-startTime')[:]
    entity_list = Entity.objects.order_by('-label')[:]
    agent_list = Agent.objects.order_by('-label')[:]
    used_list = Used.objects.order_by('-id')[:]
    wasGeneratedBy_list = WasGeneratedBy.objects.order_by('-id')[:]
    wasAssociatedWith_list = WasAssociatedWith.objects.order_by('-id')[:]
    wasAttributedTo_list = WasAttributedTo.objects.order_by('-id')[:]
    #return JsonResponse(activity_dict)
    #return render(request, 'provapp/activities.html', {'activity_list': activity_list})

    provstr = "document\n"
    for a in activity_list:
        provstr = provstr + "activity(" + a.id + ", " + str(a.startTime) + ", " + str(a.endTime) + ", [prov:type = '" + a.type + "', prov:label = '" + a.label + "', prov:description = '" + a.description + "']),\n"

    for e in entity_list:
        provstr = provstr + "entity(" + e.id + ", [prov:type = '" + e.type + "', prov:label = '" + e.label + "', prov:description = '" + e.description + "']),\n"

    for ag in agent_list:
        provstr = provstr + "agent(" + ag.id + ", [prov:type = '" + ag.type + "', prov:label = '" + ag.label + "', prov:description = '" + ag.description + "']),\n"

    for u in used_list:
        provstr = provstr + "used(" + u.activity.id + ", " + u.entity.id + ", [id = '" + str(u.id) + "', prov:role = '" + u.role + "']),\n"

    for wg in wasGeneratedBy_list:
        provstr = provstr + "wasGeneratedBy(" + wg.entity.id + ", " + wg.activity.id + ", [id = '" + str(wg.id) + "', prov:role = '" + wg.role + "']),\n"

    for wa in wasAssociatedWith_list:
        provstr = provstr + "wasAssociatedWith(" + wa.activity.id + ", " + wa.agent.id + ", [id = '" + str(wa.id) + "', prov:role = '" + wa.role + "']),\n"

    for wa in wasAttributedTo_list:
        provstr = provstr + "wasAttributedTo(" + wa.entity.id + ", " + wa.agent.id + ", [id = '" + str(wa.id) + "', prov:role = '" + wa.role + "']),\n"

    provstr += "endDocument"

    return HttpResponse(provstr, content_type='text/plain')


def provjson(request):
    """ Prov-Json serialisation as defined by W3C"""
    activity_list = Activity.objects.order_by('-startTime')[:]
    entity_list = Entity.objects.order_by('-label')[:]
    agent_list = Agent.objects.order_by('-label')[:]
    used_list = Used.objects.order_by('-id')[:]
    wasGeneratedBy_list = WasGeneratedBy.objects.order_by('-id')[:]
    wasAssociatedWith_list = WasAssociatedWith.objects.order_by('-id')[:]
    wasAttributedTo_list = WasAttributedTo.objects.order_by('-id')[:]
    #return JsonResponse(activity_dict)
    #return render(request, 'provapp/activities.html', {'activity_list': activity_list})

    # convert to json.serializable dictionaries
    prov_dict = {}
    prefix_dict = {}
    prefix_dict["prov"] = u"http://www.w3.org/ns/prov#"
    prefix_dict["xsd"] = u"http://www.w3.org/2000/10/XMLSchema#"
    prefix_dict["voprov"] = u"http://www.ivoa.com/provenancedm"
    prefix_dict["cs"] = u"http://www.cosmosim.org/prov#"
    prov_dict["prefix"] = prefix_dict

    activity_dict = {}
    for a in activity_list:
        a_dict = {}
        a_dict["prov:startTime"] = a.startTime
        a_dict["prov:endTime"] = a.endTime
        a_dict["prov:label"] = a.label
        a_dict["prov:description"] = str(a.description) 
        a_dict["voprov:type"] = str(a.type)
        a_dict["voprov:subtype"] = str(a.subtype)
        a_dict["voprov:code"] = str(a.code)
        activity_dict[a.id] = a_dict
    prov_dict["activity"] = activity_dict

    entity_dict = {}
    for e in entity_list:
        e_dict = {}
        e_dict["prov:label"] = e.label
        e_dict["prov:description"] = str(e.description) 
        e_dict["voprov:type"] = str(e.type)
        e_dict["voprov:location"] = str(e.location)
        e_dict["voprov:access"] = str(e.access)
        entity_dict[e.id] = e_dict
    prov_dict["entity"] = entity_dict

    agent_dict = {}
    for ag in agent_list:
        ag_dict = {}
        ag_dict["prov:label"] = ag.label
        #ag_dict["prov:description"] = str(ag.description) 
        ag_dict["voprov:type"] = str(ag.type)
        ag_dict["voprov:affiliation"] = ag.affiliation
        agent_dict[ag.id] = ag_dict
    prov_dict["agent"] = agent_dict

    used_dict = {}
    for u in used_list:
        u_dict = {}
        u_dict["prov:activity"] = u.activity.id
        u_dict["prov:entity"] = u.entity.id
        u_dict["voprov:role"] = u.role
        used_dict[u.id] = u_dict
    prov_dict["used"] = used_dict
  
    wasGeneratedBy_dict = {}
    for wg in wasGeneratedBy_list:
        wg_dict = {}
        wg_dict["prov:entity"] = wg.entity.id
        wg_dict["prov:activity"] = wg.activity.id
        wg_dict["voprov:role"] = wg.role
        wasGeneratedBy_dict[u.id] = wg_dict
    prov_dict["wasGeneratedBy"] = wasGeneratedBy_dict

    wasAssociatedWith_dict = {}
    for wa in wasAssociatedWith_list:
        wa_dict = {}
        wa_dict["prov:activity"] = wa.activity.id
        wa_dict["prov:agent"] = wa.agent.id
        wa_dict["voprov:role"] = wa.role
        wasAssociatedWith_dict[wa.id] = wa_dict
    prov_dict["wasAssociatedWith"] = wasAssociatedWith_dict

    wasAttributedTo_dict = {}
    for wa in wasAttributedTo_list:
        wa_dict = {}
        wa_dict["prov:entity"] = wa.entity.id
        wa_dict["prov:agent"] = wa.agent.id
        wa_dict["voprov:role"] = wa.role
        wasAttributedTo_dict[wa.id] = wa_dict
    prov_dict["wasAttributedTo"] = wasAttributedTo_dict

    #print json.dumps(prov_dict, ensure_ascii=False, indent=4).encode('utf8')
    #return HttpResponse(codecs.BOM_UTF8 + provstr.encode('utf-8'), content_type='text/plain', charset='utf-8')
    return HttpResponse(codecs.BOM_UTF8 + json.dumps(prov_dict, indent=4, ensure_ascii=False).encode('utf8'), content_type='text/plain', charset='utf-8')

def fullgraphjson(request):
    #activity = get_object_or_404(Activity, pk=activity_id)
    #return HttpResponse(json.dumps(data), content_type='application/json')
    #activity_dict = {'id': activity.id, 'label': activity.label, 'type': activity.type, 'description': activity.description}
    #activity_dict = to_dict(activity)

    activity_list = Activity.objects.all()
    entity_list = Entity.objects.all()
    agent_list = Agent.objects.all()

    used_list = Used.objects.all()
    wasGeneratedBy_list = WasGeneratedBy.objects.all()
    wasAssociatedWith_list = WasAssociatedWith.objects.all()
    wasAttributedTo_list = WasAttributedTo.objects.all()
    #hadMember_list = HadMember.objects.all()

    nodes_dict = []
    count_nodes = 0
    count_act = 0

    links_dict = []
    count_link = 0

    map_activity_ids = {}
    map_entity_ids = {}
    map_agent_ids = {}


    for a in activity_list:
        nodes_dict.append({"name": a.label, "type": "activity"})
        map_activity_ids[a.id] = count_nodes
        count_nodes = count_nodes + 1

    for e in entity_list:
        nodes_dict.append({"name": e.label, "type": "entity"})
        map_entity_ids[e.id] = count_nodes
        count_nodes = count_nodes + 1

    for ag in agent_list:
        nodes_dict.append({"name": ag.label, "type": "agent"})
        map_agent_ids[ag.id] = count_nodes
        count_nodes = count_nodes + 1

    # add links (source, target, value)
    for u in used_list:
        links_dict.append({"source": map_activity_ids[u.activity.id], "target": map_entity_ids[u.entity.id], "value": 0.5, "type": "used"})
        count_link = count_link + 1

    for w in wasGeneratedBy_list:
        links_dict.append({"source": map_entity_ids[w.entity.id], "target": map_activity_ids[w.activity.id], "value": 0.5, "type": "wasGeneratedBy"})
        count_link = count_link + 1

    for w in wasAssociatedWith_list:
        links_dict.append({"source": map_activity_ids[w.activity.id], "target": map_agent_ids[w.agent.id], "value": 0.2, "type": "wasAssociatedWith"})
        count_link = count_link + 1

    for w in wasAttributedTo_list:
        links_dict.append({"source": map_entity_ids[w.entity.id], "target": map_agent_ids[w.agent.id], "value": 0.2, "type": "wasAttributedTo"})
        count_link = count_link + 1

#    for h in hadMember_list:
#        s =  map_entity_ids[h.collection_id]
#        #print >>sys.stderr, 'h.collection_id, h.entity_id: ', h.collection_id, ", '"+h.entity_id+"'"
#        t = map_entity_ids[h.entity_id]
#        #print "map_entity_ids[h.collection_id]"
#        #links_dict.append({"source": map_entity_ids[h.collection_id], "target": map_entity_ids[h.entity_id], "value": 0.2, "type": "hadMember"})
#        links_dict.append({"source": s, "target": t, "value": 0.2, "type": "hadMember"})
#        count_link = count_link + 1


    prov_dict = {"nodes": nodes_dict, "links": links_dict}

    return JsonResponse(prov_dict)

def graphjsonact(request):
    activity = get_object_or_404(Activity, pk=activity_id)
 
    activity_list = Activity.objects.all()
    entity_list = Entity.objects.all()
    agent_list = Agent.objects.all()

    used_list = Used.objects.all()
    wasGeneratedBy_list = WasGeneratedBy.objects.all()
    wasAssociatedWith_list = WasAssociatedWith.objects.all()
    wasAttributedTo_list = WasAttributedTo.objects.all()
    #hadMember_list = HadMember.objects.all()

    nodes_dict = []
    count_nodes = 0
    count_act = 0

    links_dict = []
    count_link = 0

    map_activity_ids = {}
    map_entity_ids = {}
    map_agent_ids = {}


    for a in activity_list:
        nodes_dict.append({"name": a.label, "type": "activity"})
        map_activity_ids[a.id] = count_nodes
        count_nodes = count_nodes + 1

    for e in entity_list:
        nodes_dict.append({"name": e.label, "type": "entity"})
        map_entity_ids[e.id] = count_nodes
        count_nodes = count_nodes + 1

    for ag in agent_list:
        nodes_dict.append({"name": ag.label, "type": "agent"})
        map_agent_ids[ag.id] = count_nodes
        count_nodes = count_nodes + 1

    # add links (source, target, value)
    for u in used_list:
        links_dict.append({"source": map_activity_ids[u.activity.id], "target": map_entity_ids[u.entity.id], "value": 0.5, "type": "used"})
        count_link = count_link + 1

    for w in wasGeneratedBy_list:
        links_dict.append({"source": map_entity_ids[w.entity.id], "target": map_activity_ids[w.activity.id], "value": 0.5, "type": "wasGeneratedBy"})
        count_link = count_link + 1

    for w in wasAssociatedWith_list:
        links_dict.append({"source": map_activity_ids[w.activity.id], "target": map_agent_ids[w.agent.id], "value": 0.2, "type": "wasAssociatedWith"})
        count_link = count_link + 1

    for w in wasAttributedTo_list:
        links_dict.append({"source": map_entity_ids[w.entity.id], "target": map_agent_ids[w.agent.id], "value": 0.2, "type": "wasAttributedTo"})
        count_link = count_link + 1

    prov_dict = {"nodes": nodes_dict, "links": links_dict}
    return JsonResponse(prov_dict)
