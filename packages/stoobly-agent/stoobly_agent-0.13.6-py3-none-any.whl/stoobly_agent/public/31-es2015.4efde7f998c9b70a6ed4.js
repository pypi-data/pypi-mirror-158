(window.webpackJsonp=window.webpackJsonp||[]).push([[31],{"5Rpo":function(n,t,o){"use strict";o.r(t),o.d(t,"InvitationCallbackModuleNgFactory",function(){return g});var e=o("8Y7J");class i{}var r=o("pMnS");class s{constructor(n,t,o,e,i){this.organizationsUserResource=n,this.projectsUserResource=t,this.route=o,this.router=e,this.tokenService=i}ngOnInit(){const n=this.route.snapshot,{organization_invitation_token:t,project_invitation_token:o}=n.queryParams;if(this.tokenService.userSignedIn){let n,e;o?(n=this.projectsUserResource,e=o):t&&(n=this.organizationsUserResource,e=t),n&&e&&n.create({invitation_token:e}).subscribe(()=>{this.router.navigate(["/"])})}else this.router.navigate(["/login"],{queryParams:n.queryParams})}}var a=o("YCZM"),u=o("XTWy"),c=o("iInd"),l=o("hU4o"),b=e.yb({encapsulation:0,styles:[[""]],data:{}});function p(n){return e.bc(0,[],null,null)}function h(n){return e.bc(0,[(n()(),e.Ab(0,0,null,null,1,"stoobly-invitation-callback",[],null,null,null,p,b)),e.zb(1,114688,null,0,s,[a.a,u.a,c.a,c.p,l.c],null,null)],function(n,t){n(t,1,0)},null)}var v=e.wb("stoobly-invitation-callback",s,h,{},{},[]),k=o("SVse");class M{}var g=e.xb(i,[],function(n){return e.Lb([e.Mb(512,e.j,e.bb,[[8,[r.a,v]],[3,e.j],e.z]),e.Mb(4608,k.o,k.n,[e.w]),e.Mb(1073742336,k.c,k.c,[]),e.Mb(1073742336,c.t,c.t,[[2,c.z],[2,c.p]]),e.Mb(1073742336,M,M,[]),e.Mb(1073742336,i,i,[]),e.Mb(1024,c.n,function(){return[[{path:"",component:s}]]},[])])})}}]);