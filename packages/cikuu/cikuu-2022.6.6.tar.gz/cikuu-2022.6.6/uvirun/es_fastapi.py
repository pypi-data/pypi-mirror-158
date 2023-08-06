# 2022.7.2 cp from es_fastapi.py 
from uvirun import *
import re
requests.eshp	= os.getenv("eshp", "es.corpusly.com:9200") # host & port 

@app.get('/es/rows', tags=["es"])
def rows(query="select lem, count(*) cnt  from gzjc where type = 'tok' and pos != 'PUNCT' group by lem order by cnt desc limit 10", raw:bool=False, sum_query:str=None):
	''' # select snt from dic where type = 'snt' and kp = 'book_VERB' limit 2 
	# sum_query: select count(*) from gzjc where type='tok' '''
	res = requests.post(f"http://{requests.eshp}/_sql",json={"query": query}).json() 
	if raw: return res['rows']  
	if not sum_query is None: 
		sumi = requests.post(f"http://{requests.eshp}/_sql",json={"query": sum_query}).json()['rows'][0][0]
		return [  dict( dict(zip([ ar['name'] for ar in res['columns'] ] , ar)), **{"sumi":sumi}) for ar in res.get('rows',[]) ] 
	return [  dict(zip([ ar['name'] for ar in res['columns'] ] , ar)) for ar in res.get('rows',[]) ] 
	#return res['rows'] if raw else  [  dict(zip([ ar['name'] for ar in res['columns'] ] , ar)) for ar in res.get('rows',[]) ] 

@app.get('/es/count', tags=["es"])
def rows_count(cp:str='gzjc', type:str='snt'):
	return [ {"cnt": requests.post(f"http://{requests.eshp}/_sql",json={"query": f"select count(*) from {cp} where type = '{type}'"}).json()['rows'][0][0]} ]   

@app.get('/es/sum/{cps}/{type}', tags=["es"])
def es_sum(cps:str='gzjc,clec', type:str="snt"):
	'''  cps: gzjc,clec   type:snt   
	# [{'cp':'gzjc', 'snt': 8873}, {'cp':'clec', 'snt': 75322}] '''
	return [{"cp": cp, type: requests.post(f"http://{requests.eshp}/_sql",json={"query": f"select count(*) from {cp} where type ='{type}'"}).json()['rows'][0][0]} for cp in cps.strip().split(',')]

@app.get("/es/kwic", tags=["es"])
def corpus_kwic(cp:str='dic', w:str="opened", topk:int=10, left_tag:str="<b>", right_tag:str="</b>"): 
	''' search snt using word,  | select snt,postag, tc from gzjc where type = 'snt' and match(snt, 'books') | 2022.6.19 '''
	return [ {"snt": re.sub(rf"\b({w})\b", f"{left_tag}{w}{right_tag}", snt), "tc": tc } for snt, postag, tc in rows(f"select snt, postag, tc from {cp.strip().split(',')[0]} where type = 'snt' and match (snt, '{w}') limit {topk}", raw=True)]

@app.get('/es/outer_join', tags=["es"])
def es_outer_join(cps:str="clec,gzjc", query:str="select gov, count(*) cnt from clec where type = 'tok' and lem='door' and pos='NOUN' and dep='dobj' group by gov",  ): #perc:bool=False
	''' [{'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'clean_VERB'}, {'cp0_1': 11.0, 'cp1_1': 1.0, 'word': 'close_VERB'}, {'cp0_1': 2.0, 'cp1_1': 0.0, 'word': 'enter_VERB'}, {'cp0_1': 3.0, 'cp1_1': 0.0, 'word': 'have_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'keep_VERB'}, {'cp0_1': 3.0, 'cp1_1': 0.0, 'word': 'knock_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'lock_VERB'}, {'cp0_1': 31.0, 'cp1_1': 1.0, 'word': 'open_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'pull_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'push_VERB'}, {'cp0_1': 3.0, 'cp1_1': 0.0, 'word': 'reach_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'rush_VERB'}, {'cp0_1': 1.0, 'cp1_1': 1.0, 'word': 'shut_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'slam_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'unlock_VERB'}, {'cp0_1': 2.0, 'cp1_1': 0.0, 'word': 'watch_VERB'}, {'cp0_1': 0.0, 'cp1_1': 1.0, 'word': 'find_VERB'}, {'cp0_1': 0.0, 'cp1_1': 1.0, 'word': 'leave_VERB'}] '''
	cps = cps.strip().split(',')
	map = defaultdict(dict)
	for i, cp in enumerate(cps): 
		for row in rows(query.replace(cps[0], cp ) , raw=True): # assume the first one is the key 
			for j in range(1, len(row)): 
				map[ row[0]][ f"cp{i}_{j}"] = row[j]
	df = pd.DataFrame(map).fillna(0).transpose()
	return [ dict(dict(row), **{"word": index} ) for index, row in df.iterrows()]  #return arr[0:topk] if topk > 0  else arr 

@app.get("/es/stats", tags=["es"])
def corpus_stats(names:str=None, types:str="doc,snt,np,tok,trp,vp"):
	''' doc,snt,np,tok,simple_sent,vtov,vvbg,vp, added 2022.5.21 '''
	names = name.strip().split(',') if names else [ar['name'] for ar in sqlrows("show tables")  if not ar['name'].startswith(".") and ar['type'] == 'TABLE' and ar['kind'] == 'INDEX']
	types = types.replace(",", "','")
	return [ dict( dict(rows(f"select type, count(*) cnt from {name} where type in ('{types}') group by type")), **{"name":name} ) for name in names]

@app.post("/es/newdoc", tags=["es"])
def newdoc(arr:dict={"essay_or_snts":"The quick fox jumped over the lazy dog. The justice delayed is justice denied.", "rid":0, "uid":0}
		, index:str="shexam", gecdskhost:str='gpu120.wrask.com:8180' , refresh_index:bool=False ):  
	''' 2022.7.10 '''
	if not hasattr(newdoc, 'es'):
		from so import config
		from elasticsearch import Elasticsearch,helpers
		newdoc.es	= Elasticsearch([ f"http://{requests.eshp}"])  
	if refresh_index: newdoc.es.indices.delete(index=index)
	if not newdoc.es.indices.exists(index=index): newdoc.es.indices.create(index=index, body=config) 

	from en.esjson import sntdoc_idsour #2022.7.10
	did		= f"rid-{arr.get('rid',0)}:uid-{arr.get('uid',0)}" # filename is a kind of uid 
	requests.post(f"http://{requests.eshp}/{index}/_delete_by_query?conflicts=proceed", json={"query": { "match": { "did": did} }}).text

	dsk		= requests.post(f"http://{gecdskhost}/gecdsk", json=arr).json()
	snts	= [mkf.get('meta',{}).get('snt','') for mkf in dsk.get('snt',[])]
	arr.update({"type":"doc", "sntnum":len(snts), "score":float(dsk.get('info',{}).get("final_score",0)), "snts": json.dumps(snts) })
	newdoc.es.index(index = index,  id = did, body = arr)
	newdoc.es.index(index = index,  id = f"{did}-dims", body = dsk.get('doc',{}) )

	for i,mkf in enumerate(dsk.get('snt',[])):  
		snt = mkf.get('meta',{}).get('snt','')
		doc = spacy.nlp(snt)
		[ newdoc.es.index(index = index,  id = f"{did}:sid-{i})", body = ar['_source']) for ar in sntdoc_idsour( f"{did}:sid-{i})", snt, doc ) ]  
		[ newdoc.es.index(index = index,  id = f"{did}:sid-{i})-{v['ibeg']}", body = dict( v, **{"type":"cate", "src":f"{did}:sid-{i})"}))  for k,v in mkf.get('feedback',{}).items() if f"{did}:sid-{i})".startswith("e_") or v['cate'].startswith("w_") ]

	# add tag ,essay-level offset
	doc = spacy.nlp(arr.get('essay_or_snts',''))
	[ newdoc.es.index(index = index,  id = f"{did}:ctag-NP-{doc[np.start].idx})", body ={"type":"ctag", "ctag": "NP", "start":doc[np.start].idx, "len":len(np.text), "chunk": np.text} ) for np in doc.noun_chunks if np.end - np.start > 1]
	[ newdoc.es.index(index = index,  id = f"{did}:ctag-tok-{t.idx})", body ={"type":"ctag", "ctag": t.pos_, "start":t.idx, "len":len(t.text), "chunk": t.text} ) for t in doc if t.pos_ not in ('X','PUNCT', 'SPACY')]

	for i, sent in enumerate(doc.sents):
		sdoc = sent.as_doc()
		stag = "简单句" if len([t for t in sdoc if t.pos_ == 'VERB' and t.dep_ != 'ROOT']) <= 0 else "复杂句" 
		newdoc.es.index(index = index,  id = f"{did}:stag-{i})", body ={"type":"stag", "stag": stag, "src":f"{did}:sid-{i})", "start":sent.start, "end":sent.end, "sent": sent.text} )
		if len([t for t in sdoc if t.dep_ == 'conj' and t.head.dep_ == 'ROOT']) > 0:
			newdoc.es.index(index = index,  id = f"{did}:stag-{i}-0)", body ={"type":"stag", "stag": "复合句", "src":f"{did}:sid-{i})", "start":sent.start, "end":sent.end, "chunk": sent.text} )


@app.post("/es/uploadfile/")
async def create_upload_file(index:str="shexam", file: UploadFile = File(...), refresh_index:bool = False):
	''' folder is the index name '''
	content = await file.read()
	return indexdoc({'essay_or_snts':content.decode().strip(), 'uid':file.filename}, index=index, refresh_index=refresh_index)  

if __name__ == "__main__":   #uvicorn.run(app, host='0.0.0.0', port=80)
	#print ( rows(sum_query="select count(*) from gzjc where type='tok'") )
	print ( newdoc()) 
	#uvicorn.run(app, host='0.0.0.0', port=80)

'''
@app.get('/es/xcnt/{cp}/{type}/{column}', tags=["es"])
def corpusly_xcnt( column:str='lex', cp:str='gzjc', type:str='tok', where:str="", order:str="order by cnt desc limit 10" ):
	#column:lex, cp:gzjc, type:tok, where:  and lem='book'  | JSONCompactColumns  
	# select lex,count(*) cnt from dic where type = 'tok' and lem= 'book' group by lex 
	query  = f"select {column}, count(*) cnt from {cp} where type = '{type}' {where} group by {column} {order}"
	res = requests.post(f"http://{requests.eshp}/_sql",json={"query": query}).json() 
	return [  { column: ar[0], "cnt": ar[1]} for ar in res['rows'] ] 

@app.get("/es/srcsnts", tags=["es"])
def corpus_srcsnts(query:str="select src from gzjc where type='tok' and lem='book' and pos='NOUN' limit 10",highlight:str='book', left_tag:str="<b>", right_tag:str="</b>"):  #, cp:str='gzjc'
	cp = query.split("where")[0].strip().split('from')[-1].strip()
	srclist = "','".join([ src for src, in rows(query)])
	return [{'snt':re.sub(rf"\b({highlight})\b", f"{left_tag}{highlight}{right_tag}", snt)} for snt, in rows(f"select snt from {cp} where type='snt' and src in ('{srclist}')")]

@app.get("/es/lempos/snts", tags=["es"])
def lempos_snts(cp:str='gzjc', lem:str='book', pos:str='VERB', topk:int=3, left_tag:str="<b>", right_tag:str="</b>"): 
	# "select snt from gzjc where type = 'snt' and kp = 'book_VERB' limit 2" , added 2022.6.24 
	query = f"select snt from {cp} where type = 'snt' and kp = '{lem}_{pos}' limit {topk}"
	return [{'snt':re.sub(rf"\b({lem})\b", f"{left_tag}{lem}{right_tag}", snt)} for snt, in rows(query)]	

@app.get("/es/trp/snts", tags=["es"])
def trp_snts(cp:str='gzjc', word:str='door', rel:str='~dobj_VERB_NOUN', cur:str='open',  topk:int=3): 
	query = f"select snt from {cp} where type = 'snt' and kp = '{rel[1:]}/{cur} {word}' limit {topk}" if rel.startswith('~') else f"select snt from {cp} where type = 'snt' and kp = '{rel}/{word} {cur}' limit {topk}"
	print (query, flush=True)
	return [{'snt':snt} for snt, in rows(query)]

	#if perc: 
	#	for col in df.columns:
	#		df[f"{col}_perc"] = round((df[col] / df[col].sum()) * 100, 2)
	#if topk > 0 : df = df.sort_values(df.columns[0], ascending=False)

#sntsum	= lambda cp: requests.post(f"http://{requests.eshp}/_sql",json={"query": f"select count(*) from {cp} where type ='snt'"}).json()['rows'][0][0]
'''