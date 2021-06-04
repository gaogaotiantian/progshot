(this.webpackJsonpweb=this.webpackJsonpweb||[]).push([[0],{15:function(e,t,n){},24:function(e,t,n){},45:function(e,t,n){},59:function(e,t,n){"use strict";n.r(t);var c=n(0),s=n.n(c),r=n(26),a=n.n(r),i=(n(45),n(14)),o=n.n(i),l=n(21),u=n(11),d=(n(47),n(8)),j=(n(15),n(9)),m=n.n(j),b=(n(24),n(25),n(51),n(52),n(35)),f=n.n(b),O=n(38),h=n.n(O),x=n(39),g=n.n(x),p=n(36),v=n.n(p),N=n(37),S=n.n(N),C=n(33),k=n.n(C),y=n(1),w=function(e){var t=e.filmInfo,n=e.currFilm,c=e.setCurrFilm,s=e.sendCommand;return Object(y.jsxs)("div",{className:"source-title section-title",children:[Object(y.jsx)("div",{className:"film-name",children:t.name}),Object(y.jsxs)("div",{className:"slider-group",children:[Object(y.jsx)("input",{className:"slider",type:"range",min:"1",max:t.num_films,step:"1",value:n,onChange:function(e){return c(e.target.value)},onMouseUp:function(){return s("g "+n.toString(),"command")}}),Object(y.jsx)("div",{className:"film-number",children:n.toString()+"/"+t.num_films.toString()})]}),Object(y.jsxs)("div",{className:"btn-group",children:[Object(y.jsx)(k.a,{className:"button",title:"return",style:{fontSize:30},onClick:function(){return s("return","command")}}),Object(y.jsx)(f.a,{className:"button",fontSize:"large",onClick:function(){return s("next","command")}}),Object(y.jsx)(v.a,{className:"button",fontSize:"large",onClick:function(){return s("step","command")}}),Object(y.jsx)(S.a,{className:"button",style:{fontSize:30},onClick:function(){return s("rb","command")}}),Object(y.jsx)(h.a,{className:"button",fontSize:"large",onClick:function(){return s("back","command")}}),Object(y.jsx)(g.a,{className:"button",fontSize:"large",onClick:function(){return s("stepback","command")}})]})]})};m.a.manual=!0;var F=function(e){var t=e.currSource,n=e.currFilm,s=e.setCurrFilm,r=e.sendCommand,a=Object(c.useRef)(null);return Object(c.useEffect)((function(){m.a.highlightAllUnder(a.current)})),Object(y.jsxs)("div",{className:"section",children:[Object(y.jsx)(w,{filmInfo:t.film,currFilm:n,setCurrFilm:s,sendCommand:r}),Object(y.jsx)("div",{className:"scrollable",children:Object(y.jsx)("pre",{ref:a,id:"source-code",className:"line-numbers source","data-line":t.curr_lineno,children:Object(y.jsx)("code",{className:"source-code language-py",children:t.code})})})]})},_=(n(57),function(e){var t=e.sendCommand,n=e.addToConsoleHistory,s=e.consoleHistory,r=e.consoleOutputLines,a=Object(c.useState)(""),i=Object(u.a)(a,2),d=i[0],j=i[1],b=Object(c.useRef)(null);Object(c.useEffect)((function(){m.a.highlightAllUnder(b.current)}));var f=function(){var e=Object(l.a)(o.a.mark((function e(c){return o.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:"Enter"===c.key&&(n(d+"\n",!1),""!==d&&t(d,"console"),j(""));case 1:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}();return Object(y.jsxs)("div",{className:"section",children:[Object(y.jsx)("div",{className:"section-title",children:"Terminal"}),Object(y.jsx)("div",{className:"scrollable",children:Object(y.jsxs)("pre",{className:"command-line terminal",ref:b,"data-host":"psviewer","data-output":r,children:[Object(y.jsx)("code",{className:"language-py",children:s}),Object(y.jsx)("input",{className:"mono-word terminal-input",type:"text",id:"input",value:d,onChange:function(e){j(e.target.value)},onKeyDown:function(e){return f(e)}})]})})]})});m.a.manual=!0;var T=function(e){var t=e.currSource,n=Object(c.useRef)(null);return Object(c.useEffect)((function(){m.a.highlightAllUnder(n.current)})),Object(y.jsxs)("div",{className:"section",children:[Object(y.jsx)("div",{className:"section-title",children:"Variables"}),Object(y.jsx)("div",{className:"scrollable",children:Object(y.jsx)("pre",{className:"variables",ref:n,children:Object(y.jsx)("code",{className:"language-py",children:t.locals})})})]})},z=function(e){var t=e.active,n=e.info,c=e.sendCommand;return Object(y.jsx)("div",{className:"mono-word stack-element "+(t===n.idx?"active-stack":""),onClick:function(){return c("j "+n.idx.toString(),"command")},children:n.file_string+"\n > "+n.code_string+"\n"})},H=function(e){var t=e.stack,n=e.sendCommand;return console.log(t),Object(y.jsxs)("div",{className:"section",children:[Object(y.jsx)("div",{className:"section-title",children:"Stack"}),Object(y.jsx)("div",{className:"scrollable",children:Object(y.jsx)("div",{className:"stack",children:t.stack.map((function(e){return Object(y.jsx)(z,{active:t.curr,info:e,sendCommand:n},e.idx)}))})})]})},E=new WebSocket("ws://localhost:8080");m.a.hooks.add("complete",(function(e){if(e.element.className.includes("source-code")&&""!==e.code){var t=document.querySelector(".line-highlight"),n=t.offsetHeight,c=document.getElementById("source-code"),s=c.offsetHeight;t.scrollIntoView(!1),s>n&&c.scrollTop<=c.scrollHeight-s&&(t.offsetTop>s?c.scrollTop+=s/2:c.scrollTop+=t.offsetTop-s/2)}}));var I=function(){var e=Object(c.useState)({code:"",curr_lineno:0,locals:"",film:{name:"",num_films:0,curr_film_idx:0}}),t=Object(u.a)(e,2),n=t[0],s=t[1],r=Object(c.useState)(0),a=Object(u.a)(r,2),i=a[0],j=a[1],m=Object(c.useState)({stack:[],curr:1}),b=Object(u.a)(m,2),f=b[0],O=b[1],h=Object(c.useState)("\n"),x=Object(u.a)(h,2),g=x[0],p=x[1],v=Object(c.useState)("1"),N=Object(u.a)(v,2),S=N[0],C=N[1],k=Object(c.useState)(1),w=Object(u.a)(k,2),z=w[0],I=w[1];E.onopen=function(){E.send(JSON.stringify({type:"init"}))},E.onmessage=function(e){var t=JSON.parse(e.data);t.hasOwnProperty("source")&&(s(t.source),j(t.source.film.curr_film_idx+1)),t.hasOwnProperty("console")&&P(t.console,!0),t.hasOwnProperty("stack")&&(O(t.stack),console.log(f))};var J=function(){var e=Object(l.a)(o.a.mark((function e(t,n){var c;return o.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:c={type:n,command:t.toString()},E.send(JSON.stringify(c));case 2:case"end":return e.stop()}}),e)})));return function(t,n){return e.apply(this,arguments)}}(),P=function(e,t){var n=e;t&&A(n),p(g+n),I(z+(n.match(/\n/g)||[]).length)},A=function(e){var t=z+1,n=z+(e.match(/\n/g)||[]).length;C(S+","+t.toString()+"-"+n.toString())};return Object(y.jsx)("div",{className:"App",children:Object(y.jsxs)(d.a,{className:"container",orientation:"vertical",children:[Object(y.jsx)(d.b,{children:Object(y.jsxs)(d.a,{orientation:"horizontal",children:[Object(y.jsx)(d.b,{flex:.6,children:Object(y.jsx)(F,{currSource:n,currFilm:i,setCurrFilm:j,sendCommand:J})}),Object(y.jsx)(d.c,{}),Object(y.jsx)(d.b,{children:Object(y.jsx)(_,{sendCommand:J,addToConsoleHistory:P,consoleHistory:g,consoleOutputLines:S})})]})}),Object(y.jsx)(d.c,{}),Object(y.jsx)(d.b,{children:Object(y.jsxs)(d.a,{orientation:"horizontal",children:[Object(y.jsx)(d.b,{flex:.5,className:"stack",children:Object(y.jsx)(H,{stack:f,sendCommand:J})}),Object(y.jsx)(d.c,{}),Object(y.jsx)(d.b,{children:Object(y.jsx)(T,{currSource:n})})]})})]})})},J=function(e){e&&e instanceof Function&&n.e(3).then(n.bind(null,71)).then((function(t){var n=t.getCLS,c=t.getFID,s=t.getFCP,r=t.getLCP,a=t.getTTFB;n(e),c(e),s(e),r(e),a(e)}))};a.a.render(Object(y.jsx)(s.a.StrictMode,{children:Object(y.jsx)(I,{})}),document.getElementById("root")),J()}},[[59,1,2]]]);
//# sourceMappingURL=main.ce86c3fe.chunk.js.map