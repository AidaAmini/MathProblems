import sys
import json
import jsonrpclib
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
import pickle
brown_ic = wordnet_ic.ic('ic-brown.dat')
import unitConversion as uc
import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint
from nltk.tree import Tree

FOLD = None
NAMES = [x.strip() for x in open("names.txt").readlines()]

class aset:

    def __init__(self,num=None,entity=None,surface=None,idx=None):
        self.num = num
        self.entity = entity
        self.surface = surface
        self.idx = idx
        self.widx = (idx%1000)+1 if idx is not None else None
        self.container = None
        self.verbs = None
        self.adjs = None
        self.location = None
        self.contains = None
        self.compound = 0
        self.subtypes = []
        self.type_failure = 0
        self.origs = idx//1000 if idx is not None else None
        self.role = 'other'
        self.subset = 0

    def details(self,sf=True):

        string = "_____________\n"
        ordrd = sorted(self.__dict__.items())
        for x,y in ordrd:
            string += str(x)+" : "+str(y)+"\n"
        string += "_____________\n"
        if sf:
            print(string)
        else:
            return string

def eqvector(a,b,problem,story,target,feats=False):
    vec = vector(a,b,problem,story,target)
   
    return vec



def vector(a,b,problem,story,target,feats=False):
    a = a[1]
    b = b[1]

    vec = []
    features = []
    features.append(" a role d ")
    vec.append(int(a.role == 'do'))
    vec.append(int(a.role == 'subj'))
    vec.append(int(a.role == 'other'))
    vec.append(int(b.role == 'do'))
    vec.append(int(b.role == 'subj'))
    vec.append(int(b.role == 'other'))

    #subset
    vec.append(a.subset)
    vec.append(b.subset)

    features.append("a compound?")
    vec.append(int(a.compound))

    features.append("b compound?")
    vec.append(int(b.compound))

    features.append("a subtype of b")
    vec.append(int(a.entity in b.subtypes))

    features.append("b subtype of a")
    vec.append(int(b.entity in a.subtypes))

    features.append("a contians b entity match")
    if a.contains == None and b.entity == None: vec.append(0)
    elif a.contains == None or b.entity == None: vec.append(-1)
    elif b.entity in a.contains: vec.append(1)
    else: vec.append(-1)

    features.append("b contains a entity match")
    if b.contains == None and a.entity == None: vec.append(0)
    elif b.contains == None or a.entity == None: vec.append(-1)
    elif a.entity in b.contains: vec.append(1)
    else: vec.append(-1)


    features.append("acontainer bentity match")
    if a.container == None and b.entity == None: vec.append(0)
    elif a.container == None or b.entity == None: vec.append(-1)
    elif b.entity in a.container: vec.append(1)
    else: vec.append(-1)

    features.append("bcontainer aentity match")
    if b.container == None and a.entity == None: vec.append(0)
    elif b.container == None or a.entity == None: vec.append(-1)
    elif a.entity in b.container: vec.append(1)
    else: vec.append(-1)

    features.append("b container a entity match")
    if b.container == None and a.container == None: vec.append(0)
    elif b.container == None or a.container==None: vec.append(-1)
    else:
        #bcont = b.container.split(" ")[-1]
        #acont = a.container.split(" ")[-1]
        bcont = b.container
        acont = a.container
        if bcont in acont or acont in bcont: vec.append(1)
        else: vec.append(-1)

    features.append("entity match")
    if b.entity == None and a.entity == None: vec.append(0)
    elif b.entity == a.entity: vec.append(1)
    else: vec.append(-1)

    features.append("adj match")
    if b.adjs == None and a.adjs == None: vec.append(0)
    elif b.adjs == a.adjs: vec.append(1)
    else: vec.append(-1)

    features.append("loc match")
    if b.location == None and a.location == None: vec.append(0)
    elif b.location == a.location: vec.append(1)
    else: vec.append(-1)


    features.append('number distances')
    try:
        distance = abs(int(a.idx)-int(b.idx))
        distance = 1 / ( 10000 - distance )
    except: distance = 1
    vec.append(distance)



    features.append('x is operand')
    if a.num == 'x' or b.num=='x': vec.append(1)
    else: vec.append(0)
    features.append('x is not operand')
    if a.num =='x' or b.num == 'x': vec.append(0)
    else: vec.append(1)

    features.append('a target match')
    if a.entity==target: vec.append(1)
    else: vec.append(0)
    features.append('b target match')
    if b.entity==target: vec.append(1)
    else: vec.append(0)


    asidx = a.idx//1000
    bsidx = b.idx//1000
    story = story['sentences']
    asent = [x[0] for x in story[asidx]['words']]
    bsent = [x[0] for x in story[bsidx]['words']]
    #words inbetween features
    awidx = a.idx%1000
    bwidx = b.idx%1000
    allwords = []
    for j in range(len(story)):
        for i,x in enumerate(story[j]['words']):
            allwords.append((j*1000+i,x[0]))
    low = min(a.idx,b.idx)
    high = max(a.idx,b.idx)
    wordseg = [x[1] for x in allwords if x[0]>low and high>x[0]]
    for item in [',','and','but']:
        features.append(item)
        if item in wordseg:
            vec.append(1)
        else:
            vec.append(0)

    features.extend(["a times",'b times',"a total",'b total',"a together",'b together',"a more", 'b more' ,"a less",'b less',"a add",'b add',"a divide",'b divide',"a split",'b split',"a equal",'b equal',"a equally",'b equally'])
    for li in ["times","total","together","more","less","add","divide","split","equal","equally"]:
        if li in asent:
            vec.append(1)
        else:
            vec.append(0)
        if li in bsent: vec.append(1)
        else: vec.append(0)
    #target features
    problem = story[-1]['text'].lower()
    if " how " in problem:
        problem = problem.split(" how ")[-1]
    elif " what " in problem:
        problem = problem.split(" what ")[-1]

    if " , " in problem:
        problem = problem.split(" , ")[0]
    features.append("in all")
    if "in all" in problem: vec.append(1)
    else: vec.append(0)
    features.append("end with")
    if "end with" in problem: vec.append(1)
    else: vec.append(0)
    problem = problem.split()
    features.extend("comparatives")
    comparitive = 0
    for li in ['bigger','larger','further','farther','longer','taller']:
        if li in problem: comparitive = 1 ; break
    vec.append(comparitive)
    features.extend(["times","total","together","more","less","add","divide","split","left","equal","equally","now",'left','start'])
    for li in ["times","total","together","more","less","add","divide","split","left","equal","equally","now",'left','start']:
        if li in problem:
            vec.append(1)
        else:
            vec.append(0)

    if a.verbs == None or b.verbs == None:
        dist = 1
    else:
        avl = a.verbs.split(" ")
        bvl = b.verbs.split(" ")

        if len([x for x in avl if x in bvl ])>0:
            dist = 0
        else:
            dist = 1
            for aw in avl:
                asyns = wn.synsets(aw)
                for asyn in asyns:
                    for bw in bvl:
                        bsyns = wn.synsets(bw)
                        for bsyn in bsyns:
                            if asyn._pos == bsyn._pos: 
                                try:
                                    sim = 1/(1+bsyn.res_similarity(asyn,brown_ic))
                                except:
                                    sim = 2
                                if sim < dist:
                                    dist = sim
    features.append("Verb distance")
    vec.append(dist)

    #verb similarity
    verbs = ['be', 'do', 'go', 'have', 'leave', 'keep', 'get', 'make', 'tell', 'place', 'lose', 'change', 'give', 'hand', 'take', 'buy', 'receive', 'put', 'set', 'like', 'want', 'call', 'divide', 'split']
    #verbs = pickle.load(open('data/predicates'+FOLD,'rb'))
    #verbs = ['add','multiply','divide','subtract']

    for v in verbs:
        features.append(v)
        vsyns = wn.synsets(v, pos='v')

        dist = 1
        if b.verbs is not None:
            for verb in b.verbs.split(' '):
                bsyns = wn.synsets(verb, pos='v')
                if verb == v:
                    dist = 0
                else:
                    for vsyn in vsyns:
                        for bsyn in bsyns:
                            try:
                                sim = 1/(1+vsyn.lin_similarity(bsyn,brown_ic))
                            except:
                                sim = 2
                            if sim < dist:
                                dist = sim
        vec.append(dist)
    if feats:
        return (features, vec)
    else:
        return vec



def combine(a,b,op):
    #takes two entities and returns a combo of them.
    c = aset()
    if a.container == b.entity or op == '-':
        #multiplication or subtraction swap
        t = a
        a = b
        b = t



    for k in a.__dict__:
        if k == "num":
            c.num = "("+str(a.__dict__[k])+op+str(b.__dict__[k])+")"
        elif k in ['container','contains']:
            c.__dict__[k]=None
        else:
            c.__dict__[k]= b.__dict__[k]
    #print(c.__dict__)
    if op == '*':
        if a.entity == b.entity:
            c.type_failure = 1
    c.compound = 1
    c.subtypes = [a.entity,b.entity]
    return c

def assert_question_entity(story, sets, good):
    xset = [x for x in sets if x[1].num=='x']
    if xset and good == 0:
        xset = xset[0]
        if xset[1].entity=="NONE":
            #is there a NNS near to the question?
            words = story[-1]['words']
            idx = [x[0].lower() for x in words].index('how')
            prev = 1
            if idx>=0:
                words = words[idx:idx+4]
                nns = [x for x in words if x[1]['PartOfSpeech']=='NNS']
                if nns:
                    xset[1].entity = nns[0][1]["Lemma"]
                    xset[1].surface = nns[0][0]
                    prev = 0

            if prev:
                prev = [x for x in sets if x[0]<xset[0]]
                prev = prev[-1][1]
                xset[1].entity = prev.entity
                xset[1].surface = prev.surface

        quantifiedents = [x[1].entity for x in sets if floatcheck(x[1].num) or x[1].num=='dozen']
        if quantifiedents:
            if xset[1].entity not in quantifiedents:
                
                #change, make most prev entity rather than whatever ent
                #unless its like money or something!?
                if xset[1].entity not in ['dozen','money','$','money','cent','penny', 'nickel', 'dime', 'quarter', 'half-dollar', 'dollar', 'five-dollar bills','second', 'minute', 'hour', 'day', 'week', 'month', 'year','inches', 'feet', 'yards']:
                    xset[1].entity = quantifiedents[-1]
    return sets

def question_entity(story, sets):
    #get question entity
    ents = [x[1].entity for x in sets]
    q = story[-1]
    j = len(story)-1
    words = q["words"]
    deps = q['indexeddependencies']
    good = 0
    if "what" in [x[0].lower() for x in words]:
        targets = [x[2] for x in deps if 'what' in x[1].lower() and x[0]=='nsubj']
        if len(targets)==1:
            t,tidx = targets[0].rsplit("-",maxsplit=1)
            tidx = int(tidx)-1
            lemma = words[tidx][1]["Lemma"]
            sets.append((j*1000+tidx,aset('x',lemma,t,j*1000+tidx)))
    if "how" in [x[0].lower() for x in words]:
        targets = [x[1] for x in deps if x[2].rsplit("-",maxsplit=1)[0] in ['many','much']]
        wzeros = [x[0].lower() for x in words]
        if 'much' in wzeros:
            if ('cost' in wzeros) or ('spend' in wzeros):
                tidx = len(words)-1
                sets.append((j*1000+tidx,aset('x','dollar',"dollar",j*1000+tidx)))
                good = 1
                targets = []

        if len(targets)==1:
            t,tidx = targets[0].rsplit("-",maxsplit=1)
            tidx = int(tidx)-1
            if words[tidx][1]["PartOfSpeech"] in ["NN","NNS"]:
                lemma = words[tidx][1]["Lemma"]
                #check for dozen
                if len([x for x in deps if targets[0]==x[1] and x[0]=='nn' and 'dozen' in x[2]])>0:
                    sets.append((j*1000+tidx-1,aset('x','dozen','dozen',j*1000+tidx)))
                    sets.append((j*1000+tidx,aset('dozen',lemma,t,j*1000+tidx)))
                else:
                    sets.append((j*1000+tidx,aset('x',lemma,t,j*1000+tidx)))
                good = 1
            else:
                good = 0
                if t == "more":
                    targets = [x[1] for x in deps if x[2].rsplit("-",maxsplit=1)[0] in ['more']]
                    if targets:
                        t,tidx = targets[0].rsplit("-",maxsplit=1)
                        tidx = int(tidx)-1
                        if words[tidx][1]["PartOfSpeech"] in ["NN","NNS"]:
                            lemma = words[tidx][1]["Lemma"]
                            sets.append((j*1000+tidx,aset('x',lemma,t,j*1000+tidx)))
                            good = 1
                elif t == 'did':
                    targets = [x[2] for x in deps if x[1].rsplit("-",maxsplit=1)[0] in ['did'] and x[0]=='nsubj']
                    if targets:
                        t,tidx = targets[0].rsplit("-",maxsplit=1)
                        tidx = int(tidx)-1
                        if words[tidx][1]["PartOfSpeech"] in ["NN","NNS"]:
                            lemma = words[tidx][1]["Lemma"]
                            sets.append((j*1000+tidx,aset('x',lemma,t,j*1000+tidx)))
                            good = 1
    
                if good == 0:
                    sets.append((j*1000+tidx,aset('x','NONE','NONE',j*1000+tidx)))
                    #good = 1
        else:
            howidx = [i for i,x in enumerate(words) if x[0].lower()=='how'][0]
            nextword = words[howidx+1]
            if nextword[0] == 'far':
                sets.append((j*1000+howidx+1,aset('x','DISTANCE','DISTANCE',j*1000+howidx+1)))
                good = 1
            elif nextword[0] == 'long':
                sets.append((j*1000+howidx+1,aset('x','LENGTH','LENGTH',j*1000+howidx+1)))
                good = 1

    return (sets, good)


def extract_quantify(story):
    sets = []

    #this function makes the preliminary sets, finding the quantified entities. 
    for j,s in enumerate(story):
        deps = s['indexeddependencies']
        words = s['words']

        # nums is a list of potential entities
        nums = [(x[1],x[2]) for x in deps if x[0]=='num' or x[0]=='number' or x[0]=='det']
        #nums.extend([(x[1],x[2]) for x in deps if x[0] == 'nmod' and x[1][0].isdigit()])
        print(nums)
        nums.extend([(x[2],x[1]) for x in deps if x[0]=="prep_of" and (x[1][0].isdigit() or x[1].rsplit("-",maxsplit=1)[0] in ['half','third','quarter','some'])])
        print(nums)
        # w = word, n = number. Take each and split it out
        for w,n in nums:
            n,nidx = n.split("-")
            nidx = int(nidx)-1
            w,widx = w.rsplit("-",maxsplit=1)
            widx = int(widx)-1
            #print(w,n)

            # dealing with dollars
            if w == "$":
                lemma = 'dollar' #standardized representation of collection of forms of word
                sets.append(((j*1000)+nidx,aset(n,lemma,w,j*1000+widx)))



            elif words[widx][1]["PartOfSpeech"] in ["NN","NNS"]:
                if n=='each' and w=='cost':
                    #let this slip through
                    continue
                lemma = words[widx][1]["Lemma"]
                sets.append(((j*1000)+nidx,aset(n,lemma,w,j*1000+widx)))
                if [x for x in deps if x[0]=='prep_of' and x[1]==n and x[2]==w]:
                    sets[-1][1].subset =1

        sets = bad_parse_each(sets, words, j)


    return sets


def bad_parse_each(sets, words, j):
    surfaces = [x[0] for x in words]

    #deal with each where parse fails AND IS BAD:
    if 'each' in surfaces:
        eachi = surfaces.index('each')
        if (j*1000)+eachi in [x[0] for x in sets]:
            return sets
        setmatch = [x for x in words[eachi:eachi+4] if x[1]['Lemma'] in [y[1].entity for y in sets]]
        if setmatch and len([x for x in words[eachi:eachi+4] if x[0] in [',','and','but']])==0:
            nextword = setmatch[0]
        else:
            setmatch = [x for x in words if x[1]['Lemma'] in [y[1].entity for y in sets]]
            if setmatch:
                nextword = setmatch[0]
            else:
                nns = [x for x in words if x[1]["PartOfSpeech"]=="NNS"]
                if nns:
                    nextword = nns[-1]
        lemma = nextword[1]["Lemma"]
        sets.append(((j*1000)+eachi,aset('each',lemma,nextword[0],j*1000+eachi+1)))

    return sets

def distance(a,b,story):
    pass

def containers_dozens(sets, deps, thissentsets, j, s):
    #deal with dozens
    dozenents = [x for x in thissentsets if 'dozen' in x[1].num]
    thisdozen = [x for x in thissentsets if 'dozen' in x[1].entity]
    if dozenents:
        for x in dozenents:
            if thisdozen:
                thisdozen[0][1].contains = x[1].entity
                if thisdozen[0][1].num != 'x' and not floatcheck(thisdozen[0][1].num):
                    thisdozen[0][1].num = '1'
            else:
                dozent = aset('1','dozen','dozen',j*1000+(x[0]-1))
                dozent.contains = x[1].entity
                sets.append((x[0]-1,dozent))
                
            x[1].container = 'dozen'
            x[1].num = '12'
            


    else:
        if thisdozen:
            dozdeps = [x[2].split('-') for x in deps if 'dozen' in x[1] and 'many' not in x[0]]
            if dozdeps:
                #print(dozdeps)
                wrds = [s['words'][int(x[1])-1] for x in dozdeps]
                wrds = [x for x in wrds if x[1]['PartOfSpeech'] in ['NN','NNS']]
                if wrds:
                    wrd = wrds[0]
                    lem = wrd[1]['Lemma']
                    surf = wrd[0]
                    dozent = aset('12',lem,surf,j*1000+thisdozen[0][0]+1)
                    thisdozen[0][1].contains = lem
                    dozent.container = 'dozen'
                    sets.append((thisdozen[0][0]+1,dozent))
    return sets

def containers_each(sets, deps, thissentsets, j, s):
    #deal with each
    thiseach = [x for x in thissentsets if x[1].num in ['each','a','an','every','per','one','1']]
    if len(thiseach)>0:
        thisothers = [x for x in thissentsets if x not in thiseach]
        if thisothers:
            for eidx,e in thiseach:
                #which is closer: next ent or prev?
                if e.num in ['a','an','per']:
                    prev = [x for x in thisothers if x[0]<eidx and x[0]>eidx-5]
                    if prev:
                        target=prev[-1]
                        target[1].container = e.entity
                        e.contains = target[1].entity
                else:
                    eachdeps = [x[2] for x in deps if e.surface in x[1]]
                    eachdeps += [x[1] for x in deps if e.surface in x[2]]
                    meachdeps = [s['words'][int(x.split('-')[-1])-1][1]['Lemma'] for x in eachdeps]
                    #e.details()
                    #print(eachdeps)
                    eachdeps = [y for y in sets if floatcheck(y[1].num) and y[1].entity in meachdeps and y[1].surface + "-"+str(y[1].widx) in eachdeps]
                    #print(eachdeps,eidx)
                    if eachdeps:
                        try:
                            each0 = sorted([(abs(y[0]-eidx),y[1]) for y in eachdeps],reverse=True)[0]
                        except:
                            each0 = eachdeps[0]
                        each0[1].container = e.entity
                        e.contains = each0[1].entity
                    else:
                        prev = [x for x in thisothers if x[0]<eidx]
                        nexxt = [x for x in thisothers if x[0]>eidx]
                        if not nexxt:
                            target = prev[-1]
                        else:
                            #really should check distances, but for now lets not
                            target = nexxt[0]
                        target[1].container = e.entity
                        e.contains = target[1].entity
    return sets

def articulate(sets, deps, thissentsets, j, s):
    for e in thissentsets:

        #get verbs, adj, location
        esurface = e[1].surface+'-'+str(e[1].widx)
        #print(esurface)
        vbs = [x for x in deps if x[2]==esurface and x[0]=='dobj']
        if not vbs:
            numsurfaces = [x for x in deps if e[1].num+'-' in x[2] and x[0]=='dobj']
        if vbs:
            e[1].verbs = ' '.join([x[1].split('-')[0] for x in vbs])
            e[1].role = 'do'
        subj = [x for x in deps if x[2]==esurface and x[0]=='nsubj']
        if subj:
            e[1].role = 'subj'


        adjs = [x for x in deps if x[1]==esurface and x[0]=='amod']
        if adjs:
            e[1].adjs = ' '.join([x[2].split('-')[0] for x in adjs])

        # location
        elocs = [x[2].split("-")[0] for x in deps if x[0] in ['prep_in','prep_on','prep_at'] and x[1] == esurface]
        if elocs:
            e[1].location = ' '.join(elocs)

        if e[1].container:
            continue


        # container is nsubj
        if vbs:
            for y in vbs:
                verb = y[1]
                #deal with ditrans verbs
                if verb.split("-")[0]=='gave':
                    dtv = [x for x in deps if x[1]==verb and x[0] in ['prep_to','iobj']]
                    if dtv:
                        e[1].container = ' '.join([x[2].split('-')[0] for x in dtv])
                else:
                    #find subj, this is container
                    vsubj = [x for x in deps if x[1]==verb and x[0] in ['nsubj','nsubjpass']]
                    if vsubj:
                        e[1].container = ' '.join([x[2].split('-')[0] for x in vsubj])
        else:
            print("CONTAINER IS POSSIBLE")
            print(e[1].entity,e[1].num)
            possible_containers = [x[1].container for x in sets if x[1].container is not None]
            possible_containers = [x for x in possible_containers if x.lower() in [y[0].lower for y in s['words']]]
            if possible_containers:
                e[1].container = ' '.join(possible_containers)
        if not e[1].verbs:
            vbs = [x[1]["Lemma"] for x in s['words'] if 'VB' in x[1]['PartOfSpeech']]
            vbs2 = [x for x in vbs if x not in ['do','be','have','need']]
            if vbs2:
                e[1].verbs = ' '.join(vbs2)
            else:
                e[1].verbs = ' '.join(vbs)
    return sets

def containers(sets,story):
    for j,s in enumerate(story):
        deps = s['indexeddependencies']
        thissentsets = [x for x in sets if x[0]//1000 == j]
        sets = containers_dozens(sets, deps, thissentsets, j, s)
        sets = containers_each(sets, deps, thissentsets, j, s)
        sets = articulate(sets, deps, thissentsets, j, s)

    return sets

def floatcheck(n):
    try:
        n = ''.join([x for x in n if x!=','])
        n = float(n)
        return True
    except:
        if n == 'x': return True
        else: return False
    

def fix_each(sets):

    eaches = [x for x in sets if x[1].num in ['each','every','per','a','an','per','one']]
    for x in eaches:
        moveto = [y for y in sets if y[1].entity == x[1].entity and floatcheck(y[1].num)]
        print(moveto)
        if moveto:
            moveto = moveto[0]
            if x[0] > moveto[0]:
                moveto[1].contains = x[1].contains
                sets.remove(x)
            else:
                x[1].contains = moveto[1].contains
                x[1].num = moveto[1].num
                sets.remove(moveto)
        else:
            x[1].num == '1'

    i=0
    while i<len(sets):
        if sets[i][1].container:
            containers = [x for x in sets if x[1].entity == sets[i][1].container and x[1].contains == sets[i][1].entity and floatcheck(x[1].num)]
            if containers:
                sets[i] = (containers[0][0]+1,sets[i][1])
        i+=1

    '''
    for i in range(len(sets)):
        idx,e = sets[i]
        #if e.num in ['each','a','an','the','every']:
        if e.contains is not None:
            #others = [x for x in sets if x[1].entity == e.entity and x[0] != idx and len([y for y in x[1].num if y.isdigit()])>0]
            #if len(others)>=1:
                if len(sets)>i+1:
                    if sets[i+1][1].entity == e.contains:
                        if sets[i+1][1].num == 'x':
                            #move x to set
                            sets[i+1] = (idx-1,sets[i+1][1])
                        else:
                            idx = sets[i+1][0]+1
                            sets[i] = (idx,e)
                        
                #e.num = '1'
            others = [x for x in sets if x[1].entity == e.entity and x[0] != idx]
            others = [x for x in others if x[1].num=='x' or floatcheck(x[1].num)]
            onum = [x[1].num for x in others]
            if 'x' in onum:
                e.num = 'x'
            elif others:
                prev = [x for x in others if x[0]<idx]
                if prev:
                    prev = prev[-1]
                    idx = sets.index(prev)
                    sets[idx]
                    e.num = prev[-1][1].num
                    prev[-1][1].num = "USED"
                else:
                    e.num = others[0][1].num
                    others[0][1].num="USED"
    '''
                
    return sets

        
def circumscription(story, sets):
    for j,s in enumerate(story):
        print s
        deps = s['indexeddependencies']
        words = s['words']
        othernums = [((j*1000+i), x[0]) for i,x in enumerate(words) if x[1]["PartOfSpeech"]=="CD"]
        othernums = [x for x in othernums if x[0] not in [y[0] for y in sets]]
        if othernums:
            for idx,n in othernums:
                prev=1
                #this is a hack To fix the "and" bug
                if 'and' in [x[0] for x in words[idx%1000:idx%1000+7]]:
                    #use next jawn
                    nextjawn = [x for x in sets if x[0]>idx and x[0]<(((idx//1000)+1)*1000)]
                    if nextjawn:
                        nextjawn = nextjawn[0][1]
                        sets.append((idx,aset(n,nextjawn.entity,nextjawn.surface,j*1000+idx)))
                        prev=0
                if prev==1:
                    prevjawn = [x for x in sets if x[0]<idx]
                    if prevjawn:
                        #prev quantified jawns:
                        pqjawns = [x for x in prevjawn if floatcheck(x[1].num)]
                        if pqjawns:
                            prevjawn = pqjawns[-1][1]
                        else:
                            prevjawn = prevjawn[-1][1]
                        sets.append((idx,aset(n,prevjawn.entity,prevjawn.surface,j*1000+idx)))
                    else:
                        #find the NNSess
                        #print(idx,n)
                        nns = []
                        for j,s in enumerate(story):
                            nns.extend([(j*1000+i,w) for i,w in enumerate(s['words']) if w[1]["PartOfSpeech"] == "NNS"])
                        #print(nns)
                        if nns:
                            prev = [x[1] for x in nns if x[0]<idx]
                            if prev:
                                prevjawn = prev[-1]
                                sets.append((idx,aset(n,prevjawn[1]["Lemma"],prevjawn[0],j*1000+idx)))
                            else:
                                prevjawn = nns[0][1]
                                sets.append((idx,aset(n,prevjawn[1]["Lemma"],prevjawn[0],j*1000+idx)))
    return sets


def add_bare_sets(sets,story):
    quantifiedents = [x[1].entity for x in sets if floatcheck(x[1].num) or x[1].num in ['dozen','half']]
    #print(quantifiedents)
    
    for j,s in enumerate(story):
        thissentsets = [x for x in sets if x[0]//1000 == j]
        thissentids = [x[1].widx for x in thissentsets]
        for i,w in enumerate(s['words']):
            if i+1 in thissentids:
                continue
            if w[1]['Lemma'] in quantifiedents:
                sets.append(((j*1000)+i,aset('BARE',w[1]['Lemma'],w[0],j*1000+i)))

    return sets

def fix_times(sets):
    times = [x for x in sets if x[1].entity == 'time']
    if times:
        for x in times:
            pcontainer = [y[1].container for y in sets if y[0] < x[0] and y[1].container != None]
            if pcontainer:
                x[1].entity = pcontainer[-1]
    return sets

def move_x(sets,story):
    targets = [(i,x) for i,x in enumerate(sets) if x[1].num == 'x']
    if not targets:
        return sets
    target = targets[0][1][1].entity

    #first process question
    q = story[-1]
    j = len(story)-1
    startwords = ['begin','start']
    endwords = ['leave','remain','finish']
    qlem = [x[1]['Lemma'] for x in q['words']]
    if len([x for x in startwords if x in qlem])>0:
        #move x to beginning
        sets[targets[0][0]] = (0,targets[0][1][1])
        return sets
    if len([x for x in endwords if x in qlem])>0:
        return sets

    options = [(i,x) for i,x in enumerate(sets) if x[1].num in ['some'] and x[1].entity == target]
    if options:
        i,x = options[0]
        sets[i][1].num = 'x'
        del(sets[targets[0][0]])
        print("Moved X Based on Some, The")


    return sets

def fix_half(sets):
    halves = [x for x in sets if x[1].num=='half']
    for i,x in halves:
        x.num = '0.5'
        x.container = x.entity
        x.entity = 'half'
    return sets
    
def coref(sets):
    pros = [x for x in sets if x[1].container != None]
    pros = [x for x in pros if x[1].container.lower() in ['he','she','her','his','him']]
    for pro in pros:
        others = [x for x in sets if x[1].container != None]
        others = [x[1].container for x in others if x[1].container[0].isupper() and x[0]<pro[0]]
        if others:
            pro[1].container = others[-1]
    return sets

def oneEnt(sets):
    notx = [x[1].entity for x in sets if x[1].num!='x']
    if not notx:
        return sets
    notx = list(set(notx))
    if len(notx)==1:     
        x = [x[1] for x in sets if x[1].num=='x']
        if not x:
            sets.append((10000,aset('x',list(notx)[0],'none',0)))
        else:
            x = x[0]
            x.entity = list(notx)[0]
    return sets

def oneSet(sets,story):
    qsets = [x for x in sets if x[1].num!="x"]
    if len(qsets)==1:
        place = qsets[0][0]
        allwords = ' '.join([story[i]['text'] for i in range(len(story))])
        allwords = ''.join([x for x in allwords if x.isalnum() or x==' '])
        if 'week' in allwords or "Week" in allwords:
            sets.append((0,aset('7','day','week',place+1)))
        else:
            names = []
            for s in story:
                names.extend([x[0] for x in s['words'] if x[1]["NamedEntityTag"]=='PERSON'])
            
            n = len(set(names))
            sets.append((place+1,aset(str(n),'person','names',place+1)))
    return sets
            
def xAdjFix(sets):
    exes = [x[1] for x in sets if x[1].num=='x']
    for x in exes:
        if x.adjs == None: continue
        adjs = x.adjs.split(" ")
        adjs = [y for y in adjs if y not in ['many','much']]
        if len(adjs)==0:
            x.adjs = None
        else:
            x.adjs = " ".join(adjs)
    return sets

def makesets(story):
    sets = extract_quantify(story)
    print([(x[0],x[1].num) for x in sets])
    (sets, good) = question_entity(story, sets)
    sets = circumscription(story, sets)            
    sets = assert_question_entity(story, sets, good)
    print([(x[0],x[1].num) for x in sets])
    sets = sorted(sets)
    # print("ee")
    # print([(x[0],x[1].entity,x[1].num) for x in sets])
    sets = fix_half(sets)
    sets = containers(sets,story)
    #sets = circumscription(sets,story)
    #sets = oneSet(sets,story)
    sets = add_bare_sets(sets,story)
    # print("units and bare sets")
    # print([(x[0],x[1].entity,x[1].num) for x in sets])
    sets = fix_each(sets)
    sets = fix_times(sets)
    print([(x[0],x[1].num) for x in sets])
    # print('eac')
    # print([(x[0],x[1].entity,x[1].num) for x in sets])
    sets = move_x(sets,story)
    sets = coref(sets)
    # print('mov x')
    # print([(x[0],x[1].entity,x[1].num) for x in sets])
    # print('target entity fix')
    #sets = oneEnt(sets)
    sets = xAdjFix(sets)
    sets = [x for x in sets if (floatcheck(x[1].num) or x[1].num=='x')]
    (sets, conv) = uc.main(sets)
    if conv == 0:
        sets = oneSet(sets, story)
    print([(x[0],x[1].num) for x in sets])
    # is there x?
    exes = [x for x in sets if x[1].num=='x']
    if not exes:
        sets.append((1000*(len(story)-1),aset('x','UNKNOWN','UNKNOWN',10000)))

    #sets = prune(sets)
    #print([(x[0],x[1].entity,x[1].num) for x in sets])
    #rewrite(sets,story)
    
    #fix idx
    for idx,x in sets:
        x.idx = idx
    try:
        sets = sorted(sets)               
    except:
        #print(sets)
        #exec(input())
        pass

    return sets

class StanfordNLP:
    def __init__(self):
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 8080)))
    
    def parse(self, text):
        return json.loads(self.server.parse(text))

def parse_inp(inp):
    q=[]
    a=[]
    e=[]
    with open(inp) as f:
        f = f.readlines()
        i=0
        while i<len(f):
            q.append(f[i])
            i+=1
            e.append(f[i])
            i+=1
            a.append(f[i])
            i+=1
    return (q,a,e)


if __name__ == "__main__":
    nlp = StanfordNLP()
    for i in range(67 , 514):
        print i
        # 12, 66
        # if i == 17 or i == 30 or i == 33 or i == 70 or i == 104 or i == 106 or i ==132 or i == 151 or i == 215 or i == 246 or i == 200 or i == 281 or i == 283 or i == 308 or i == 312 or i == 335 or i == 375:
        #     continue
        input_file = open("data/problems/"+str(i) + '.txt', 'r')
        problem = input_file.readline()
        outputfile = open("data/parse_trees/"+str(i)+ ".txt", 'w')
        story = nlp.parse(problem)['sentences']
        from nltk.tree import Tree
        # outputfile.write(str(story))
        # outputfile.write('\n')
        for sentence in story:
            # print sentence
            tree = Tree.fromstring(sentence['parsetree'])
            outputfile.write(str(tree) + '\n')
    # q,a,e = parse_inp(sys.argv[1])
    # wps = q
    # while True:
    #     for i in range(len(q)):
    #         print(i, q[i])
    #         outputfile = open("parse_stan_corenlp"+str(i)+ ".txt", 'w')
    #         problem = wps[i]
    #         story = nlp.parse(problem)
    #         outputfile.write(str(story["sentences"]))
    #     k = input()
    #     k=int(k)
    #     problem = wps[k]

    #     print(problem)
    #     # client_nlp = client.client()
    #     story = nlp.parse(problem)
    #     # print story
    #     sets = makesets(story["sentences"])
    #     for s in sets: s[1].details()
    #     input()


