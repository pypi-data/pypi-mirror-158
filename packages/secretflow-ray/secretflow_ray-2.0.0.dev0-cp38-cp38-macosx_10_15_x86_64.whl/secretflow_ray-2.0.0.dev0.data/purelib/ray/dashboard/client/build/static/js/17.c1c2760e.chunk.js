(this.webpackJsonpclient=this.webpackJsonpclient||[]).push([[17],{754:function(e,a,t){"use strict";t.r(a);var n=t(8),l=t(12),r=t(217),c=t(178),o=t(715),i=t(716),m=t(225),s=t(171),u=t(749),d=t(742),p=t(233),E=t(176),b=t(755),h=t(91),f=t(734),g=t(735),k=t(736),v=t(737),y=t(738),j=t(739),O=t(740),w=t(741),I=t(743),N=t(714),x=t.n(N),C=t(0),S=t.n(C),D=t(127),R=t(748),T=t(728),P=t(170),B=t(174),J=t(79),A=t(732),G=t(733),L=t(35),_=function(e){return function(e,a){for(var t=[];e.length;)t.push(e.splice(0,a));return t}(e.split(""),2).reverse().map((function(e){return e.join("")})).join("")},F=Object(h.a)((function(e){return{toolContainer:{background:e.palette.primary.main,width:48,height:48,borderRadius:48,position:"fixed",bottom:100,left:50,color:e.palette.primary.contrastText},icon:{position:"absolute",left:12,cursor:"pointer",top:12},popover:{position:"absolute",left:50,bottom:48,width:500,height:300,padding:6,border:"1px solid",borderColor:e.palette.text.disabled},close:{float:"right",color:e.palette.error.main,cursor:"pointer"}}})),M=function(){var e=Object(C.useState)(""),a=Object(n.a)(e,2),t=a[0],l=a[1];return S.a.createElement("div",{style:{padding:8}},S.a.createElement(D.a,{style:{width:"100%"},id:"standard-basic",label:"Object Id",InputProps:{onChange:function(e){var a=e.target.value;l(a)}}}),S.a.createElement("div",null,40===t.length?S.a.createElement("div",{style:{padding:8}},"Job ID: ",t.slice(24,28)," ",S.a.createElement("br",null),"Actor ID: ",t.slice(16,28)," ",S.a.createElement("br",null),"Task ID: ",t.slice(0,28)," ",S.a.createElement("br",null),"Index: ",parseInt(_(t.slice(32)),16)," ",S.a.createElement("br",null),"Flag: ",_(t.slice(28,32)),S.a.createElement("br",null),S.a.createElement("br",null),[["Create From Task",15,1],["Put Object",14,0],["Return Object",14,1]].filter((function(e){var a,l,r,c=Object(n.a)(e,3),o=(c[0],c[1]),i=c[2];return a=_(t.slice(28,32)),l=o,r=parseInt(a,16),Number(!!(r&1<<l))===i})).map((function(e){var a=Object(n.a)(e,1)[0];return S.a.createElement(L.a,{key:a,type:"tag",status:a})}))):S.a.createElement("span",{style:{color:J.a[500]}},"Object ID should be 40 letters long")))},U=function(){var e=Object(C.useState)("oid_converter"),a=Object(n.a)(e,2),t=a[0],l=a[1],r={oid_converter:S.a.createElement(M,null)};return S.a.createElement("div",null,S.a.createElement(R.a,{value:t,onChange:function(e,a){return l(a)}},S.a.createElement(T.a,{value:"oid_converter",label:S.a.createElement("span",{style:{fontSize:12}},"Object ID Reader")})),r[t])},z=function(){var e=Object(C.useState)(!1),a=Object(n.a)(e,2),t=a[0],l=a[1],r=F();return S.a.createElement(P.a,{className:r.toolContainer},S.a.createElement(A.a,{className:r.icon,onClick:function(){return l(!t)}}),S.a.createElement(B.a,{in:t,style:{transformOrigin:"300 500 0"}},S.a.createElement(P.a,{className:r.popover},S.a.createElement(G.a,{className:r.close,onClick:function(){return l(!1)}}),S.a.createElement(U,null))))},H=t(114),V=t.n(H),Y=t(45),q=Object(h.a)((function(e){return{root:Object(l.a)({display:"flex","& a":{color:e.palette.primary.main}},e.breakpoints.down("md"),{paddingTop:64}),drawer:Object(l.a)({width:200,flexShrink:0,background:e.palette.background.paper},e.breakpoints.up("md"),{width:200,flexShrink:0}),drawerPaper:{width:200,border:"none",background:e.palette.background.paper,boxShadow:e.shadows[1]},title:{padding:e.spacing(2),textAlign:"center",lineHeight:"36px"},divider:{background:"rgba(255, 255, 255, .12)"},menuItem:{cursor:"pointer","&:hover":{background:e.palette.primary.main}},menuIcon:{color:e.palette.text.secondary},selected:{background:"linear-gradient(45deg, ".concat(e.palette.primary.main," 30%, ").concat(e.palette.secondary.main," 90%)")},child:{flex:1},appBar:Object(l.a)({},e.breakpoints.up("md"),{width:"calc(100% - ".concat(200,"px)"),marginLeft:200}),menuButton:Object(l.a)({marginRight:e.spacing(2)},e.breakpoints.up("md"),{display:"none"}),toolbar:e.mixins.toolbar,content:{flexGrow:1,padding:e.spacing(3)}}}));a.default=function(e){var a=q(),t=e.location,l=e.history,h=e.children,N=e.setTheme,D=e.theme,R=Object(C.useState)(!1),T=Object(n.a)(R,2),P=T[0],B=T[1],J=function(){B(!P)},A=S.a.createElement(r.a,null,S.a.createElement(c.a,{button:!0,className:x()(a.menuItem,"/"===t.pathname&&a.selected),onClick:function(){return l.push("/")}},S.a.createElement(o.a,null,S.a.createElement(f.a,{className:a.menuIcon})),S.a.createElement(i.a,null,"SUMMARY")),S.a.createElement(c.a,{button:!0,className:x()(a.menuItem,t.pathname.includes("node")&&a.selected),onClick:function(){return l.push("/node")}},S.a.createElement(o.a,null,S.a.createElement(g.a,{className:a.menuIcon})),S.a.createElement(i.a,null,"NODES")),S.a.createElement(c.a,{button:!0,className:x()(a.menuItem,t.pathname.includes("job")&&a.selected),onClick:function(){return l.push("/job")}},S.a.createElement(o.a,null,S.a.createElement(k.a,{className:a.menuIcon})),S.a.createElement(i.a,null,"JOBS")),S.a.createElement(c.a,{button:!0,className:x()(a.menuItem,t.pathname.includes("event")&&a.selected),onClick:function(){return l.push("/event")}}," ",S.a.createElement(o.a,null,S.a.createElement(v.a,{className:a.menuIcon})),S.a.createElement(i.a,null,"EVENTS")),S.a.createElement(c.a,{button:!0,className:x()(a.menuItem,t.pathname.includes("log")&&a.selected),onClick:function(){return l.push("/log")}},S.a.createElement(o.a,null,S.a.createElement(y.a,{className:a.menuIcon})),S.a.createElement(i.a,null,"LOGS")),S.a.createElement(c.a,null,S.a.createElement(m.a,{color:"primary",onClick:function(){window.scrollTo(0,0)}},S.a.createElement(s.a,{title:"Back To Top"},S.a.createElement(j.a,null))),S.a.createElement(m.a,{color:"primary",onClick:function(){N("dark"===D?"light":"dark")}},S.a.createElement(s.a,{title:"Theme - ".concat(D)},"dark"===D?S.a.createElement(O.a,null):S.a.createElement(w.a,null)))),S.a.createElement(z,null));return S.a.createElement("div",{className:a.root},S.a.createElement(Y.b,{title:""}),S.a.createElement(u.a,{lgUp:!0,implementation:"css"},S.a.createElement(d.a,{color:"inherit"},S.a.createElement(p.a,null,S.a.createElement(m.a,{onClick:J},S.a.createElement(I.a,null)),S.a.createElement(E.a,{variant:"h6",style:{flexGrow:1,marginLeft:16}},"RayDashboard"))),S.a.createElement(b.a,{anchor:"left",classes:{paper:a.drawerPaper},open:P,onClose:J},S.a.createElement(E.a,{variant:"h6",className:a.title},S.a.createElement("img",{width:48,src:V.a,alt:"Ray"})," ",S.a.createElement("br",null)," Ray Dashboard"),A)),S.a.createElement(u.a,{mdDown:!0,implementation:"css"},S.a.createElement(b.a,{variant:"permanent",anchor:"left",className:a.drawer,classes:{paper:a.drawerPaper}},S.a.createElement(E.a,{variant:"h6",className:a.title},S.a.createElement("img",{width:48,src:V.a,alt:"Ray"})," ",S.a.createElement("br",null)," Ray Dashboard"),A)),S.a.createElement("div",{className:a.child},h))}}}]);