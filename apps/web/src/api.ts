export const API_URL=import.meta.env.VITE_API_URL??"http://127.0.0.1:8000";
export type Source={chunk_id:string;document_id:string;filename:string;content:string;retrieval_score:number;rerank_score:number};
export type QueryResponse={query:string;answer:string|null;confidence:number;citations:Array<{source:number;claim:string}>;sources:Source[];sub_queries:string[]};
export type Document={id:string;filename:string;content_type:string;size_bytes:number;chunks:number};
export async function queryRag(query:string):Promise<QueryResponse>{const r=await fetch(`${API_URL}/query`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({query,top_k:5})});if(!r.ok)throw Error(await r.text());return r.json();}
export async function uploadDocument(file:File):Promise<Document>{const f=new FormData();f.append("file",file);const r=await fetch(`${API_URL}/documents/upload`,{method:"POST",body:f});if(!r.ok)throw Error(await r.text());return r.json();}
export async function listDocuments():Promise<Document[]>{const r=await fetch(`${API_URL}/documents`);if(!r.ok)throw Error(await r.text());return r.json();}
