!function(){function l(l,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");l.prototype=Object.create(t&&t.prototype,{constructor:{value:l,writable:!0,configurable:!0}}),t&&n(l,t)}function n(l,t){return(n=Object.setPrototypeOf||function(l,n){return l.__proto__=n,l})(l,t)}function t(l){var n=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],function(){})),!0}catch(l){return!1}}();return function(){var t,u=i(l);if(n){var a=i(this).constructor;t=Reflect.construct(u,arguments,a)}else t=u.apply(this,arguments);return e(this,t)}}function e(l,n){return!n||"object"!=typeof n&&"function"!=typeof n?function(l){if(void 0===l)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return l}(l):n}function i(l){return(i=Object.setPrototypeOf?Object.getPrototypeOf:function(l){return l.__proto__||Object.getPrototypeOf(l)})(l)}function u(l,n){if(!(l instanceof n))throw new TypeError("Cannot call a class as a function")}function a(l,n){for(var t=0;t<n.length;t++){var e=n[t];e.enumerable=e.enumerable||!1,e.configurable=!0,"value"in e&&(e.writable=!0),Object.defineProperty(l,e.key,e)}}function r(l,n,t){return n&&a(l.prototype,n),t&&a(l,t),l}(window.webpackJsonp=window.webpackJsonp||[]).push([[5],{"4GLy":function(l,n,t){"use strict";t.d(n,"a",function(){return a});var e=t("8Y7J"),i=t("iCaw"),a=function(){var l=function(){function l(n){u(this,l),this.restApi=n,this.ENDPOINT="aliases"}return r(l,[{key:"index",value:function(l){return this.restApi.index([this.ENDPOINT],l)}},{key:"show",value:function(l,n){return this.restApi.show([this.ENDPOINT,l],n)}},{key:"create",value:function(l){return this.restApi.create([this.ENDPOINT],l)}},{key:"update",value:function(l,n){return this.restApi.update([this.ENDPOINT,l],n)}},{key:"destroy",value:function(l,n){return this.restApi.destroy([this.ENDPOINT,l],n)}}]),l}();return l.\u0275prov=e.cc({factory:function(){return new l(e.dc(i.a))},token:l,providedIn:"root"}),l}()},"81Fm":function(l,n,t){"use strict";t.d(n,"a",function(){return P});var e=t("8Y7J"),i=t("CeGm"),u=t("UhP/"),a=t("H3DK"),r=t("VDRc"),o=t("/q54"),c=t("Q2Ze"),s=t("9gLZ"),d=t("SCoL"),b=t("omvX"),f=t("Y1Mv"),m=t("ZTz/"),h=t("s7LF"),p=t("7KAL"),g=t("YEUz"),v=t("SVse"),O=t("iELJ"),y=t("1Xc+"),_=t("Dxy4"),z=t("XE/z"),I=t("Tj54"),x=t("l+Q0"),k=t("cUpR"),C=t("mGvx"),w=t("BSbQ"),S=t("e6WT"),F=t("8sFK"),A=t("zDob"),j=e.yb({encapsulation:0,styles:[[""]],data:{}});function N(l){return e.bc(0,[(l()(),e.Ab(0,0,null,null,2,"mat-option",[["class","mat-option mat-focus-indicator"],["role","option"]],[[1,"tabindex",0],[2,"mat-selected",null],[2,"mat-option-multiple",null],[2,"mat-active",null],[8,"id",0],[1,"aria-selected",0],[1,"aria-disabled",0],[2,"mat-option-disabled",null]],[[null,"click"],[null,"keydown"]],function(l,n,t){var i=!0;return"click"===n&&(i=!1!==e.Ob(l,1)._selectViaInteraction()&&i),"keydown"===n&&(i=!1!==e.Ob(l,1)._handleKeydown(t)&&i),i},i.c,i.a)),e.zb(1,8568832,[[19,4]],0,u.q,[e.l,e.h,[2,u.j],[2,u.i]],{value:[0,"value"]},null),(l()(),e.Yb(2,0,[" "," "]))],function(l,n){l(n,1,0,n.context.$implicit)},function(l,n){l(n,0,0,e.Ob(n,1)._getTabIndex(),e.Ob(n,1).selected,e.Ob(n,1).multiple,e.Ob(n,1).active,e.Ob(n,1).id,e.Ob(n,1)._getAriaSelected(),e.Ob(n,1).disabled.toString(),e.Ob(n,1).disabled),l(n,2,0,n.context.$implicit)})}function L(l){return e.bc(0,[(l()(),e.Ab(0,0,null,null,27,"mat-form-field",[["class","mat-form-field"],["fxFlex","20"]],[[2,"mat-form-field-appearance-standard",null],[2,"mat-form-field-appearance-fill",null],[2,"mat-form-field-appearance-outline",null],[2,"mat-form-field-appearance-legacy",null],[2,"mat-form-field-invalid",null],[2,"mat-form-field-can-float",null],[2,"mat-form-field-should-float",null],[2,"mat-form-field-has-label",null],[2,"mat-form-field-hide-placeholder",null],[2,"mat-form-field-disabled",null],[2,"mat-form-field-autofilled",null],[2,"mat-focused",null],[2,"mat-accent",null],[2,"mat-warn",null],[2,"ng-untouched",null],[2,"ng-touched",null],[2,"ng-pristine",null],[2,"ng-dirty",null],[2,"ng-valid",null],[2,"ng-invalid",null],[2,"ng-pending",null],[2,"_mat-animation-noopable",null]],null,null,a.b,a.a)),e.zb(1,737280,null,0,r.b,[e.l,o.i,o.e,r.h,o.f],{fxFlex:[0,"fxFlex"]},null),e.zb(2,7520256,null,9,c.g,[e.l,e.h,e.l,[2,s.b],[2,c.c],d.a,e.B,[2,b.a]],null,null),e.Ub(603979776,10,{_controlNonStatic:0}),e.Ub(335544320,11,{_controlStatic:0}),e.Ub(603979776,12,{_labelChildNonStatic:0}),e.Ub(335544320,13,{_labelChildStatic:0}),e.Ub(603979776,14,{_placeholderChild:0}),e.Ub(603979776,15,{_errorChildren:1}),e.Ub(603979776,16,{_hintChildren:1}),e.Ub(603979776,17,{_prefixChildren:1}),e.Ub(603979776,18,{_suffixChildren:1}),e.Tb(2048,null,c.b,null,[c.g]),(l()(),e.Ab(13,0,null,3,2,"mat-label",[],null,null,null,null,null)),e.zb(14,16384,[[12,4],[13,4]],0,c.k,[],null,null),(l()(),e.Yb(-1,null,["Type"])),(l()(),e.Ab(16,0,null,1,11,"mat-select",[["aria-autocomplete","none"],["aria-haspopup","true"],["class","mat-select"],["formControlName","type"],["role","combobox"]],[[2,"ng-untouched",null],[2,"ng-touched",null],[2,"ng-pristine",null],[2,"ng-dirty",null],[2,"ng-valid",null],[2,"ng-invalid",null],[2,"ng-pending",null],[1,"id",0],[1,"tabindex",0],[1,"aria-controls",0],[1,"aria-expanded",0],[1,"aria-label",0],[1,"aria-required",0],[1,"aria-disabled",0],[1,"aria-invalid",0],[1,"aria-describedby",0],[1,"aria-activedescendant",0],[2,"mat-select-disabled",null],[2,"mat-select-invalid",null],[2,"mat-select-required",null],[2,"mat-select-empty",null],[2,"mat-select-multiple",null]],[[null,"keydown"],[null,"focus"],[null,"blur"]],function(l,n,t){var i=!0;return"keydown"===n&&(i=!1!==e.Ob(l,21)._handleKeydown(t)&&i),"focus"===n&&(i=!1!==e.Ob(l,21)._onFocus()&&i),"blur"===n&&(i=!1!==e.Ob(l,21)._onBlur()&&i),i},f.b,f.a)),e.Tb(6144,null,u.j,null,[m.d]),e.zb(18,671744,null,0,h.j,[[3,h.d],[8,null],[8,null],[8,null],[2,h.z]],{name:[0,"name"]},null),e.Tb(2048,null,h.p,null,[h.j]),e.zb(20,16384,null,0,h.q,[[4,h.p]],null,null),e.zb(21,2080768,null,3,m.d,[p.e,e.h,e.B,u.d,e.l,[2,s.b],[2,h.s],[2,h.k],[2,c.b],[6,h.p],[8,null],m.b,g.k,[2,m.a]],null,null),e.Ub(603979776,19,{options:1}),e.Ub(603979776,20,{optionGroups:1}),e.Ub(603979776,21,{customTrigger:0}),e.Tb(2048,[[10,4],[11,4]],c.h,null,[m.d]),(l()(),e.jb(16777216,null,1,1,null,N)),e.zb(27,278528,null,0,v.l,[e.R,e.O,e.u],{ngForOf:[0,"ngForOf"]},null)],function(l,n){var t=n.component;l(n,1,0,"20"),l(n,18,0,"type"),l(n,21,0),l(n,27,0,t.formOptions.pathSegmentTypes)},function(l,n){l(n,0,1,["standard"==e.Ob(n,2).appearance,"fill"==e.Ob(n,2).appearance,"outline"==e.Ob(n,2).appearance,"legacy"==e.Ob(n,2).appearance,e.Ob(n,2)._control.errorState,e.Ob(n,2)._canLabelFloat(),e.Ob(n,2)._shouldLabelFloat(),e.Ob(n,2)._hasFloatingLabel(),e.Ob(n,2)._hideControlPlaceholder(),e.Ob(n,2)._control.disabled,e.Ob(n,2)._control.autofilled,e.Ob(n,2)._control.focused,"accent"==e.Ob(n,2).color,"warn"==e.Ob(n,2).color,e.Ob(n,2)._shouldForward("untouched"),e.Ob(n,2)._shouldForward("touched"),e.Ob(n,2)._shouldForward("pristine"),e.Ob(n,2)._shouldForward("dirty"),e.Ob(n,2)._shouldForward("valid"),e.Ob(n,2)._shouldForward("invalid"),e.Ob(n,2)._shouldForward("pending"),!e.Ob(n,2)._animationsEnabled]),l(n,16,1,[e.Ob(n,20).ngClassUntouched,e.Ob(n,20).ngClassTouched,e.Ob(n,20).ngClassPristine,e.Ob(n,20).ngClassDirty,e.Ob(n,20).ngClassValid,e.Ob(n,20).ngClassInvalid,e.Ob(n,20).ngClassPending,e.Ob(n,21).id,e.Ob(n,21).tabIndex,e.Ob(n,21).panelOpen?e.Ob(n,21).id+"-panel":null,e.Ob(n,21).panelOpen,e.Ob(n,21).ariaLabel||null,e.Ob(n,21).required.toString(),e.Ob(n,21).disabled.toString(),e.Ob(n,21).errorState,e.Ob(n,21)._ariaDescribedby||null,e.Ob(n,21)._getAriaActiveDescendant(),e.Ob(n,21).disabled,e.Ob(n,21).errorState,e.Ob(n,21).required,e.Ob(n,21).empty,e.Ob(n,21).multiple])})}function T(l){return e.bc(0,[e.Qb(0,v.x,[]),(l()(),e.Ab(1,0,null,null,64,"form",[["novalidate",""]],[[2,"ng-untouched",null],[2,"ng-touched",null],[2,"ng-pristine",null],[2,"ng-dirty",null],[2,"ng-valid",null],[2,"ng-invalid",null],[2,"ng-pending",null]],[[null,"ngSubmit"],[null,"submit"],[null,"reset"]],function(l,n,t){var i=!0,u=l.component;return"submit"===n&&(i=!1!==e.Ob(l,3).onSubmit(t)&&i),"reset"===n&&(i=!1!==e.Ob(l,3).onReset()&&i),"ngSubmit"===n&&(i=!1!==u.create()&&i),i},null,null)),e.zb(2,16384,null,0,h.A,[],null,null),e.zb(3,540672,null,0,h.k,[[8,null],[8,null]],{form:[0,"form"]},{ngSubmit:"ngSubmit"}),e.Tb(2048,null,h.d,null,[h.k]),e.zb(5,16384,null,0,h.r,[[6,h.d]],null,null),(l()(),e.Ab(6,0,null,null,13,"div",[["class","mat-dialog-title"],["fxLayout","row"],["fxLayoutAlign","start center"],["mat-dialog-title",""]],[[8,"id",0]],null,null,null,null)),e.zb(7,671744,null,0,r.d,[e.l,o.i,r.k,o.f],{fxLayout:[0,"fxLayout"]},null),e.zb(8,671744,null,0,r.c,[e.l,o.i,r.i,o.f],{fxLayoutAlign:[0,"fxLayoutAlign"]},null),e.zb(9,81920,null,0,O.m,[[2,O.l],e.l,O.e],null,null),(l()(),e.Ab(10,0,null,null,3,"h2",[["class","headline m-0"],["fxFlex","auto"]],null,null,null,null,null)),e.zb(11,737280,null,0,r.b,[e.l,o.i,o.e,r.h,o.f],{fxFlex:[0,"fxFlex"]},null),(l()(),e.Yb(12,null,[""," ",""])),e.Sb(13,1),(l()(),e.Ab(14,0,null,null,5,"button",[["class","text-secondary mat-focus-indicator"],["mat-dialog-close",""],["mat-icon-button",""],["type","button"]],[[1,"aria-label",0],[1,"type",0],[1,"disabled",0],[2,"_mat-animation-noopable",null],[2,"mat-button-disabled",null]],[[null,"click"]],function(l,n,t){var i=!0;return"click"===n&&(i=!1!==e.Ob(l,15)._onButtonClick(t)&&i),i},y.d,y.b)),e.zb(15,606208,null,0,O.g,[[2,O.l],e.l,O.e],{type:[0,"type"],dialogResult:[1,"dialogResult"]},null),e.zb(16,4374528,null,0,_.b,[e.l,g.h,[2,b.a]],null,null),(l()(),e.Ab(17,0,null,0,2,"mat-icon",[["class","mat-icon notranslate"],["role","img"]],[[1,"data-mat-icon-type",0],[1,"data-mat-icon-name",0],[1,"data-mat-icon-namespace",0],[2,"mat-icon-inline",null],[2,"mat-icon-no-color",null],[2,"ic-inline",null],[4,"font-size",null],[8,"innerHTML",1]],null,null,z.b,z.a)),e.zb(18,8634368,null,0,I.b,[e.l,I.d,[8,null],I.a,e.n],null,null),e.zb(19,606208,null,0,x.a,[k.b],{icIcon:[0,"icIcon"]},null),(l()(),e.Ab(20,0,null,null,1,"mat-divider",[["class","-mx-6 text-border mat-divider"],["role","separator"]],[[1,"aria-orientation",0],[2,"mat-divider-vertical",null],[2,"mat-divider-horizontal",null],[2,"mat-divider-inset",null]],null,null,C.b,C.a)),e.zb(21,49152,null,0,w.a,[],null,null),(l()(),e.Ab(22,0,null,null,34,"mat-dialog-content",[["class","mt-6 mat-dialog-content"],["fxLayout","row"],["fxLayoutGap","10px"]],null,null,null,null,null)),e.zb(23,671744,null,0,r.d,[e.l,o.i,r.k,o.f],{fxLayout:[0,"fxLayout"]},null),e.zb(24,1720320,null,0,r.e,[e.l,e.B,s.b,o.i,r.j,o.f],{fxLayoutGap:[0,"fxLayoutGap"]},null),e.zb(25,16384,null,0,O.j,[],null,null),(l()(),e.Ab(26,0,null,null,28,"mat-form-field",[["class","mat-form-field"],["fxFlex",""]],[[2,"mat-form-field-appearance-standard",null],[2,"mat-form-field-appearance-fill",null],[2,"mat-form-field-appearance-outline",null],[2,"mat-form-field-appearance-legacy",null],[2,"mat-form-field-invalid",null],[2,"mat-form-field-can-float",null],[2,"mat-form-field-should-float",null],[2,"mat-form-field-has-label",null],[2,"mat-form-field-hide-placeholder",null],[2,"mat-form-field-disabled",null],[2,"mat-form-field-autofilled",null],[2,"mat-focused",null],[2,"mat-accent",null],[2,"mat-warn",null],[2,"ng-untouched",null],[2,"ng-touched",null],[2,"ng-pristine",null],[2,"ng-dirty",null],[2,"ng-valid",null],[2,"ng-invalid",null],[2,"ng-pending",null],[2,"_mat-animation-noopable",null]],null,null,a.b,a.a)),e.zb(27,737280,null,0,r.b,[e.l,o.i,o.e,r.h,o.f],{fxFlex:[0,"fxFlex"]},null),e.zb(28,7520256,null,9,c.g,[e.l,e.h,e.l,[2,s.b],[2,c.c],d.a,e.B,[2,b.a]],null,null),e.Ub(603979776,1,{_controlNonStatic:0}),e.Ub(335544320,2,{_controlStatic:0}),e.Ub(603979776,3,{_labelChildNonStatic:0}),e.Ub(335544320,4,{_labelChildStatic:0}),e.Ub(603979776,5,{_placeholderChild:0}),e.Ub(603979776,6,{_errorChildren:1}),e.Ub(603979776,7,{_hintChildren:1}),e.Ub(603979776,8,{_prefixChildren:1}),e.Ub(603979776,9,{_suffixChildren:1}),e.Tb(2048,null,c.b,null,[c.g]),(l()(),e.Ab(39,0,null,3,2,"mat-label",[],null,null,null,null,null)),e.zb(40,16384,[[3,4],[4,4]],0,c.k,[],null,null),(l()(),e.Yb(-1,null,["Name"])),(l()(),e.Ab(42,0,null,1,7,"input",[["cdkFocusInitial",""],["class","mat-input-element mat-form-field-autofill-control"],["formControlName","name"],["matInput",""]],[[2,"ng-untouched",null],[2,"ng-touched",null],[2,"ng-pristine",null],[2,"ng-dirty",null],[2,"ng-valid",null],[2,"ng-invalid",null],[2,"ng-pending",null],[2,"mat-input-server",null],[1,"id",0],[1,"data-placeholder",0],[8,"disabled",0],[8,"required",0],[1,"readonly",0],[1,"aria-invalid",0],[1,"aria-required",0]],[[null,"input"],[null,"blur"],[null,"compositionstart"],[null,"compositionend"],[null,"focus"]],function(l,n,t){var i=!0;return"input"===n&&(i=!1!==e.Ob(l,43)._handleInput(t.target.value)&&i),"blur"===n&&(i=!1!==e.Ob(l,43).onTouched()&&i),"compositionstart"===n&&(i=!1!==e.Ob(l,43)._compositionStart()&&i),"compositionend"===n&&(i=!1!==e.Ob(l,43)._compositionEnd(t.target.value)&&i),"focus"===n&&(i=!1!==e.Ob(l,48)._focusChanged(!0)&&i),"blur"===n&&(i=!1!==e.Ob(l,48)._focusChanged(!1)&&i),"input"===n&&(i=!1!==e.Ob(l,48)._onInput()&&i),i},null,null)),e.zb(43,16384,null,0,h.e,[e.G,e.l,[2,h.a]],null,null),e.Tb(1024,null,h.o,function(l){return[l]},[h.e]),e.zb(45,671744,null,0,h.j,[[3,h.d],[8,null],[8,null],[6,h.o],[2,h.z]],{name:[0,"name"]},null),e.Tb(2048,null,h.p,null,[h.j]),e.zb(47,16384,null,0,h.q,[[4,h.p]],null,null),e.zb(48,5128192,null,0,S.a,[e.l,d.a,[6,h.p],[2,h.s],[2,h.k],u.d,[8,null],F.a,e.B,[2,c.b]],null,null),e.Tb(2048,[[1,4],[2,4]],c.h,null,[S.a]),(l()(),e.Ab(50,0,null,0,4,"mat-icon",[["class","ltr:mr-3 rtl:ml-3 mat-icon notranslate"],["matPrefix",""],["role","img"]],[[1,"data-mat-icon-type",0],[1,"data-mat-icon-name",0],[1,"data-mat-icon-namespace",0],[2,"mat-icon-inline",null],[2,"mat-icon-no-color",null],[2,"ic-inline",null],[4,"font-size",null],[8,"innerHTML",1]],null,null,z.b,z.a)),e.zb(51,16384,null,0,c.l,[],null,null),e.zb(52,8634368,null,0,I.b,[e.l,I.d,[8,null],I.a,e.n],null,null),e.zb(53,606208,null,0,x.a,[k.b],{icIcon:[0,"icIcon"]},null),e.Tb(2048,[[8,4]],c.d,null,[c.l]),(l()(),e.jb(16777216,null,null,1,null,L)),e.zb(56,16384,null,0,v.m,[e.R,e.O],{ngIf:[0,"ngIf"]},null),(l()(),e.Ab(57,0,null,null,8,"mat-dialog-actions",[["align","end"],["class","mat-dialog-actions"]],null,null,null,null,null)),e.zb(58,16384,null,0,O.f,[],null,null),(l()(),e.Ab(59,0,null,null,3,"button",[["class","mat-focus-indicator"],["mat-button",""],["mat-dialog-close",""],["type","button"]],[[1,"aria-label",0],[1,"type",0],[1,"disabled",0],[2,"_mat-animation-noopable",null],[2,"mat-button-disabled",null]],[[null,"click"]],function(l,n,t){var i=!0;return"click"===n&&(i=!1!==e.Ob(l,60)._onButtonClick(t)&&i),i},y.d,y.b)),e.zb(60,606208,null,0,O.g,[[2,O.l],e.l,O.e],{type:[0,"type"],dialogResult:[1,"dialogResult"]},null),e.zb(61,4374528,null,0,_.b,[e.l,g.h,[2,b.a]],null,null),(l()(),e.Yb(-1,0,["CANCEL"])),(l()(),e.Ab(63,0,null,null,2,"button",[["class","mat-focus-indicator"],["color","primary"],["mat-button",""],["type","submit"]],[[1,"disabled",0],[2,"_mat-animation-noopable",null],[2,"mat-button-disabled",null]],null,null,y.d,y.b)),e.zb(64,4374528,null,0,_.b,[e.l,g.h,[2,b.a]],{color:[0,"color"]},null),(l()(),e.Yb(-1,0,["SUBMIT"]))],function(l,n){var t=n.component;l(n,3,0,t.form),l(n,7,0,"row"),l(n,8,0,"start center"),l(n,9,0),l(n,11,0,"auto"),l(n,15,0,"button",""),l(n,18,0),l(n,19,0,t.icClose),l(n,23,0,"row"),l(n,24,0,"10px"),l(n,27,0,""),l(n,45,0,"name"),l(n,48,0),l(n,52,0),l(n,53,0,t.icLink),l(n,56,0,t.isPathSegment()),l(n,60,0,"button",""),l(n,64,0,"primary")},function(l,n){var t=n.component;l(n,1,0,e.Ob(n,5).ngClassUntouched,e.Ob(n,5).ngClassTouched,e.Ob(n,5).ngClassPristine,e.Ob(n,5).ngClassDirty,e.Ob(n,5).ngClassValid,e.Ob(n,5).ngClassInvalid,e.Ob(n,5).ngClassPending),l(n,6,0,e.Ob(n,9).id);var i=e.Zb(n,12,0,l(n,13,0,e.Ob(n,0),t.mode));l(n,12,0,i,t.getTitle()),l(n,14,0,e.Ob(n,15).ariaLabel||null,e.Ob(n,15).type,e.Ob(n,16).disabled||null,"NoopAnimations"===e.Ob(n,16)._animationMode,e.Ob(n,16).disabled),l(n,17,0,e.Ob(n,18)._usingFontIcon()?"font":"svg",e.Ob(n,18)._svgName||e.Ob(n,18).fontIcon,e.Ob(n,18)._svgNamespace||e.Ob(n,18).fontSet,e.Ob(n,18).inline,"primary"!==e.Ob(n,18).color&&"accent"!==e.Ob(n,18).color&&"warn"!==e.Ob(n,18).color,e.Ob(n,19).inline,e.Ob(n,19).size,e.Ob(n,19).iconHTML),l(n,20,0,e.Ob(n,21).vertical?"vertical":"horizontal",e.Ob(n,21).vertical,!e.Ob(n,21).vertical,e.Ob(n,21).inset),l(n,26,1,["standard"==e.Ob(n,28).appearance,"fill"==e.Ob(n,28).appearance,"outline"==e.Ob(n,28).appearance,"legacy"==e.Ob(n,28).appearance,e.Ob(n,28)._control.errorState,e.Ob(n,28)._canLabelFloat(),e.Ob(n,28)._shouldLabelFloat(),e.Ob(n,28)._hasFloatingLabel(),e.Ob(n,28)._hideControlPlaceholder(),e.Ob(n,28)._control.disabled,e.Ob(n,28)._control.autofilled,e.Ob(n,28)._control.focused,"accent"==e.Ob(n,28).color,"warn"==e.Ob(n,28).color,e.Ob(n,28)._shouldForward("untouched"),e.Ob(n,28)._shouldForward("touched"),e.Ob(n,28)._shouldForward("pristine"),e.Ob(n,28)._shouldForward("dirty"),e.Ob(n,28)._shouldForward("valid"),e.Ob(n,28)._shouldForward("invalid"),e.Ob(n,28)._shouldForward("pending"),!e.Ob(n,28)._animationsEnabled]),l(n,42,1,[e.Ob(n,47).ngClassUntouched,e.Ob(n,47).ngClassTouched,e.Ob(n,47).ngClassPristine,e.Ob(n,47).ngClassDirty,e.Ob(n,47).ngClassValid,e.Ob(n,47).ngClassInvalid,e.Ob(n,47).ngClassPending,e.Ob(n,48)._isServer,e.Ob(n,48).id,e.Ob(n,48).placeholder,e.Ob(n,48).disabled,e.Ob(n,48).required,e.Ob(n,48).readonly&&!e.Ob(n,48)._isNativeSelect||null,e.Ob(n,48).errorState,e.Ob(n,48).required.toString()]),l(n,50,0,e.Ob(n,52)._usingFontIcon()?"font":"svg",e.Ob(n,52)._svgName||e.Ob(n,52).fontIcon,e.Ob(n,52)._svgNamespace||e.Ob(n,52).fontSet,e.Ob(n,52).inline,"primary"!==e.Ob(n,52).color&&"accent"!==e.Ob(n,52).color&&"warn"!==e.Ob(n,52).color,e.Ob(n,53).inline,e.Ob(n,53).size,e.Ob(n,53).iconHTML),l(n,59,0,e.Ob(n,60).ariaLabel||null,e.Ob(n,60).type,e.Ob(n,61).disabled||null,"NoopAnimations"===e.Ob(n,61)._animationMode,e.Ob(n,61).disabled),l(n,63,0,e.Ob(n,64).disabled||null,"NoopAnimations"===e.Ob(n,64)._animationMode,e.Ob(n,64).disabled)})}var P=e.wb("aliases-create",A.a,function(l){return e.bc(0,[(l()(),e.Ab(0,0,null,null,1,"aliases-create",[],null,null,null,T,j)),e.zb(1,114688,null,0,A.a,[O.a,O.l,h.g],null,null)],function(l,n){l(n,1,0)},null)},{mode:"mode",source:"source"},{},[])},"9Gk2":function(l,n){n.__esModule=!0,n.default={body:'<path opacity=".3" d="M4 18h16V6H4v12zm7.5-11c2.49 0 4.5 2.01 4.5 4.5c0 .88-.26 1.69-.7 2.39l2.44 2.43l-1.42 1.42l-2.44-2.44c-.69.44-1.51.7-2.39.7C9.01 16 7 13.99 7 11.5S9.01 7 11.5 7z" fill="currentColor"/><path d="M11.49 16c.88 0 1.7-.26 2.39-.7l2.44 2.44l1.42-1.42l-2.44-2.43c.44-.7.7-1.51.7-2.39C16 9.01 13.99 7 11.5 7S7 9.01 7 11.5S9.01 16 11.49 16zm.01-7a2.5 2.5 0 0 1 0 5a2.5 2.5 0 0 1 0-5zM20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V6h16v12z" fill="currentColor"/>',width:24,height:24}},C0s9:function(l,n,t){"use strict";t.d(n,"a",function(){return e});var e=function l(){u(this,l)}},CwgZ:function(l,n){n.__esModule=!0,n.default={body:'<path d="M12 3L2 12h3v8h6v-6h2v6h6v-8h3L12 3zm5 15h-2v-6H9v6H7v-7.81l5-4.5l5 4.5V18z" fill="currentColor"/><path opacity=".3" d="M7 10.19V18h2v-6h6v6h2v-7.81l-5-4.5z" fill="currentColor"/>',width:24,height:24}},DaE0:function(l,n){n.__esModule=!0,n.default={body:'<path opacity=".3" d="M22 15c0-1.66-1.34-3-3-3h-1.5v-.5C17.5 8.46 15.04 6 12 6c-.77 0-1.49.17-2.16.46L20.79 17.4c.73-.55 1.21-1.41 1.21-2.4zM2 14c0 2.21 1.79 4 4 4h9.73l-8-8H6c-2.21 0-4 1.79-4 4z" fill="currentColor"/><path d="M19.35 10.04A7.49 7.49 0 0 0 12 4c-1.33 0-2.57.36-3.65.97l1.49 1.49C10.51 6.17 11.23 6 12 6c3.04 0 5.5 2.46 5.5 5.5v.5H19a2.996 2.996 0 0 1 1.79 5.4l1.41 1.41c1.09-.92 1.8-2.27 1.8-3.81c0-2.64-2.05-4.78-4.65-4.96zM3 5.27l2.77 2.77h-.42A5.994 5.994 0 0 0 0 14c0 3.31 2.69 6 6 6h11.73l2 2l1.41-1.41L4.41 3.86L3 5.27zM7.73 10l8 8H6c-2.21 0-4-1.79-4-4s1.79-4 4-4h1.73z" fill="currentColor"/>',width:24,height:24}},De0L:function(l,n){n.__esModule=!0,n.default={body:'<path opacity=".3" d="M12.07 6.01c-3.87 0-7 3.13-7 7s3.13 7 7 7s7-3.13 7-7s-3.13-7-7-7zm1 8h-2v-6h2v6z" fill="currentColor"/><path d="M9.07 1.01h6v2h-6zm2 7h2v6h-2zm8.03-.62l1.42-1.42c-.43-.51-.9-.99-1.41-1.41l-1.42 1.42A8.962 8.962 0 0 0 12.07 4c-4.97 0-9 4.03-9 9s4.02 9 9 9A8.994 8.994 0 0 0 19.1 7.39zm-7.03 12.62c-3.87 0-7-3.13-7-7s3.13-7 7-7s7 3.13 7 7s-3.13 7-7 7z" fill="currentColor"/>',width:24,height:24}},Ell1:function(l,n){n.__esModule=!0,n.default={body:'<circle cx="9" cy="8.5" opacity=".3" r="1.5" fill="currentColor"/><path opacity=".3" d="M4.34 17h9.32c-.84-.58-2.87-1.25-4.66-1.25s-3.82.67-4.66 1.25z" fill="currentColor"/><path d="M9 12c1.93 0 3.5-1.57 3.5-3.5S10.93 5 9 5S5.5 6.57 5.5 8.5S7.07 12 9 12zm0-5c.83 0 1.5.67 1.5 1.5S9.83 10 9 10s-1.5-.67-1.5-1.5S8.17 7 9 7zm0 6.75c-2.34 0-7 1.17-7 3.5V19h14v-1.75c0-2.33-4.66-3.5-7-3.5zM4.34 17c.84-.58 2.87-1.25 4.66-1.25s3.82.67 4.66 1.25H4.34zm11.7-3.19c1.16.84 1.96 1.96 1.96 3.44V19h4v-1.75c0-2.02-3.5-3.17-5.96-3.44zM15 12c1.93 0 3.5-1.57 3.5-3.5S16.93 5 15 5c-.54 0-1.04.13-1.5.35c.63.89 1 1.98 1 3.15s-.37 2.26-1 3.15c.46.22.96.35 1.5.35z" fill="currentColor"/>',width:24,height:24}},KNdO:function(l,n,t){"use strict";t.d(n,"a",function(){return d}),t.d(n,"b",function(){return v});var e=t("8Y7J"),i=t("iInd"),a=t("SVse"),o=function(){function l(){u(this,l)}return r(l,[{key:"ngOnInit",value:function(){}}]),l}(),c=e.yb({encapsulation:2,styles:[],data:{}});function s(l){return e.bc(0,[e.Nb(null,0)],null,null)}t("Z998");var d=e.yb({encapsulation:0,styles:[["span[_ngcontent-%COMP%]{color:#000}"]],data:{}});function b(l){return e.bc(0,[(l()(),e.Ab(0,0,null,null,0,"div",[["class","w-1 h-1 bg-gray-300 rounded-full ltr:mr-2 rtl:ml-2"]],null,null,null,null,null))],null,null)}function f(l){return e.bc(0,[(l()(),e.Ab(0,0,null,null,3,"a",[],[[1,"target",0],[8,"href",4]],[[null,"click"]],function(l,n,t){var i=!0;return"click"===n&&(i=!1!==e.Ob(l,1).onClick(t.button,t.ctrlKey,t.shiftKey,t.altKey,t.metaKey)&&i),i},null,null)),e.zb(1,671744,null,0,i.s,[i.p,i.a,a.i],{queryParams:[0,"queryParams"],routerLink:[1,"routerLink"]},null),(l()(),e.Yb(2,null,[" "," "])),e.Qb(0,a.w,[])],function(l,n){l(n,1,0,n.parent.context.$implicit.queryParams,n.parent.context.$implicit.routerLink)},function(l,n){l(n,0,0,e.Ob(n,1).target,e.Ob(n,1).href),l(n,2,0,n.parent.context.$implicit.name.length>100?e.Zb(n,2,0,e.Ob(n,3).transform(n.parent.context.$implicit.name,0,100))+"...":n.parent.context.$implicit.name)})}function m(l){return e.bc(0,[(l()(),e.Ab(0,0,null,null,2,"a",[["class","cursor-pointer"]],null,[[null,"click"]],function(l,n,t){var e=!0;return"click"===n&&(e=!1!==l.component.select.emit(l.parent.parent.context.$implicit.data)&&e),e},null,null)),(l()(),e.Yb(1,null,[" "," "])),e.Qb(0,a.w,[])],null,function(l,n){l(n,1,0,n.parent.parent.context.$implicit.name.length>100?e.Zb(n,1,0,e.Ob(n,2).transform(n.parent.parent.context.$implicit.name,0,100))+"...":n.parent.parent.context.$implicit.name)})}function h(l){return e.bc(0,[(l()(),e.Ab(0,0,null,null,2,"span",[],null,null,null,null,null)),(l()(),e.Yb(1,null,[" "," "])),e.Qb(0,a.w,[])],null,function(l,n){l(n,1,0,n.parent.parent.context.$implicit.name.length>100?e.Zb(n,1,0,e.Ob(n,2).transform(n.parent.parent.context.$implicit.name,0,100))+"...":n.parent.parent.context.$implicit.name)})}function p(l){return e.bc(0,[(l()(),e.jb(16777216,null,null,1,null,m)),e.zb(1,16384,null,0,a.m,[e.R,e.O],{ngIf:[0,"ngIf"],ngIfElse:[1,"ngIfElse"]},null),(l()(),e.jb(0,[["elseBlock",2]],null,0,null,h))],function(l,n){l(n,1,0,n.component.select.observers.length>0&&n.parent.context.$implicit.data,e.Ob(n,2))},null)}function g(l){return e.bc(0,[(l()(),e.Ab(0,0,null,null,7,null,null,null,null,null,null,null)),(l()(),e.jb(16777216,null,null,1,null,b)),e.zb(2,16384,null,0,a.m,[e.R,e.O],{ngIf:[0,"ngIf"]},null),(l()(),e.Ab(3,0,null,null,4,"vex-breadcrumb",[["class","vex-breadcrumb body-2 text-hint leading-none hover:text-primary-500 no-underline trans-ease-out ltr:mr-2 rtl:ml-2"]],null,null,null,s,c)),e.zb(4,114688,null,0,o,[],null,null),(l()(),e.jb(16777216,null,0,1,null,f)),e.zb(6,16384,null,0,a.m,[e.R,e.O],{ngIf:[0,"ngIf"],ngIfElse:[1,"ngIfElse"]},null),(l()(),e.jb(0,[["elseIfBlock",2]],0,0,null,p))],function(l,n){l(n,2,0,0!==n.context.index),l(n,4,0),l(n,6,0,n.context.$implicit.routerLink,e.Ob(n,7))},null)}function v(l){return e.bc(0,[(l()(),e.Ab(0,0,null,null,2,"div",[["class","flex items-center"]],null,null,null,null,null)),(l()(),e.jb(16777216,null,null,1,null,g)),e.zb(2,278528,null,0,a.l,[e.R,e.O,e.u],{ngForOf:[0,"ngForOf"],ngForTrackBy:[1,"ngForTrackBy"]},null)],function(l,n){var t=n.component;l(n,2,0,t.crumbs,t.trackByValue)},null)}},"PB+l":function(l,n,t){"use strict";t.d(n,"a",function(){return e});var e=function l(){u(this,l)}},SqwC:function(l,n){n.__esModule=!0,n.default={body:'<path d="M6 10c-1.1 0-2 .9-2 2s.9 2 2 2s2-.9 2-2s-.9-2-2-2zm12 0c-1.1 0-2 .9-2 2s.9 2 2 2s2-.9 2-2s-.9-2-2-2zm-6 0c-1.1 0-2 .9-2 2s.9 2 2 2s2-.9 2-2s-.9-2-2-2z" fill="currentColor"/>',width:24,height:24}},Z998:function(l,n,t){"use strict";t.d(n,"a",function(){return c});var e=t("8Y7J"),i=t("CwgZ"),a=t.n(i),o=t("zK3P"),c=function(){function l(){u(this,l),this.crumbs=[],this.select=new e.o,this.trackByValue=o.c,this.icHome=a.a}return r(l,[{key:"ngOnInit",value:function(){}}]),l}()},"h+Y6":function(l,n){n.__esModule=!0,n.default={body:'<path d="M17 7h-4v2h4c1.65 0 3 1.35 3 3s-1.35 3-3 3h-4v2h4c2.76 0 5-2.24 5-5s-2.24-5-5-5zm-6 8H7c-1.65 0-3-1.35-3-3s1.35-3 3-3h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-2zm-3-4h8v2H8z" fill="currentColor"/>',width:24,height:24}},qJKI:function(l,n,t){"use strict";t.d(n,"a",function(){return o});var e=t("8Y7J"),i=t("4UAC"),a=t("msBP"),o=function(){var l=function(){function l(n,t){u(this,l),this.projectResource=n,this.projectDataService=t}return r(l,[{key:"resolve",value:function(l){return this.projectDataService.get(l.queryParams.project_id||l.params.project_id||l.parent.params.project_id)}}]),l}();return l.\u0275prov=e.cc({factory:function(){return new l(e.dc(i.a),e.dc(a.a))},token:l,providedIn:"root"}),l}()},tq8E:function(n,e,i){"use strict";i.d(e,"a",function(){return m}),i.d(e,"b",function(){return h}),i.d(e,"c",function(){return v}),i.d(e,"d",function(){return b}),i.d(e,"e",function(){return p}),i.d(e,"f",function(){return g}),i.d(e,"g",function(){return f}),i.d(e,"h",function(){return c});var a=i("8Y7J"),o=i("mrSG"),c=function l(){u(this,l)};function s(l){return null!=l&&""+l!="false"}var d=function(l){return l[l.BACKSPACE=8]="BACKSPACE",l[l.DELETE=46]="DELETE",l}({}),b=function(){function l(n){u(this,l),this.sanitizer=n,this._removable=!1,this.removed=new a.o,this.tabIndex=0}return r(l,[{key:"keyEvent",value:function(l){switch(l.keyCode){case d.BACKSPACE:case d.DELETE:this.remove()}}},{key:"_remove",value:function(l){l.stopPropagation(),this.remove()}},{key:"remove",value:function(){this._removable&&this.removed.next(this.file)}},{key:"readFile",value:function(){return Object(o.a)(this,void 0,void 0,regeneratorRuntime.mark(function l(){var n=this;return regeneratorRuntime.wrap(function(l){for(;;)switch(l.prev=l.next){case 0:return l.abrupt("return",new Promise(function(l,t){var e=new FileReader;if(e.onload=function(n){l(n.target.result)},e.onerror=function(l){console.error("FileReader failed on file ".concat(n.file.name,".")),t(l)},!n.file)return t("No file to read. Please provide a file using the [file] Input property.");e.readAsDataURL(n.file)}));case 1:case"end":return l.stop()}},l)}))}},{key:"removable",get:function(){return this._removable},set:function(l){this._removable=s(l)}},{key:"hostStyle",get:function(){return this.sanitizer.bypassSecurityTrustStyle("\n\t\t\tdisplay: flex;\n\t\t\theight: 140px;\n\t\t\tmin-height: 140px;\n\t\t\tmin-width: 180px;\n\t\t\tmax-width: 180px;\n\t\t\tjustify-content: center;\n\t\t\talign-items: center;\n\t\t\tpadding: 0 20px;\n\t\t\tmargin: 10px;\n\t\t\tborder-radius: 5px;\n\t\t\tposition: relative;\n\t\t")}}]),l}(),f=function(){function l(){u(this,l)}return r(l,[{key:"parseFileList",value:function(l,n,t,e){for(var i=[],u=[],a=0;a<l.length;a++){var r=l.item(a);this.isAccepted(r,n)?t&&r.size>t?this.rejectFile(u,r,"size"):!e&&i.length>=1?this.rejectFile(u,r,"no_multiple"):i.push(r):this.rejectFile(u,r,"type")}return{addedFiles:i,rejectedFiles:u}}},{key:"isAccepted",value:function(l,n){if("*"===n)return!0;var t=n.split(",").map(function(l){return l.toLowerCase().trim()}),e=l.type.toLowerCase(),i=l.name.toLowerCase();return!!t.find(function(l){return l.endsWith("/*")?e.split("/")[0]===l.split("/")[0]:l.startsWith(".")?i.endsWith(l):l==e})}},{key:"rejectFile",value:function(l,n,t){var e=n;e.reason=t,l.push(e)}}]),l}(),m=function(){function l(n){u(this,l),this.service=n,this.change=new a.o,this.accept="*",this._disabled=!1,this._multiple=!0,this._maxFileSize=void 0,this._expandable=!1,this._disableClick=!1,this._isHovered=!1}return r(l,[{key:"_onClick",value:function(){this.disableClick||this.showFileSelector()}},{key:"_onDragOver",value:function(l){this.disabled||(this.preventDefault(l),this._isHovered=!0)}},{key:"_onDragLeave",value:function(){this._isHovered=!1}},{key:"_onDrop",value:function(l){this.disabled||(this.preventDefault(l),this._isHovered=!1,this.handleFileDrop(l.dataTransfer.files))}},{key:"showFileSelector",value:function(){this.disabled||this._fileInput.nativeElement.click()}},{key:"_onFilesSelected",value:function(l){this.handleFileDrop(l.target.files),this._fileInput.nativeElement.value="",this.preventDefault(l)}},{key:"handleFileDrop",value:function(l){var n=this.service.parseFileList(l,this.accept,this.maxFileSize,this.multiple);this.change.next({addedFiles:n.addedFiles,rejectedFiles:n.rejectedFiles,source:this})}},{key:"preventDefault",value:function(l){l.preventDefault(),l.stopPropagation()}},{key:"_hasPreviews",get:function(){return!!this._previewChildren.length}},{key:"disabled",get:function(){return this._disabled},set:function(l){this._disabled=s(l),this._isHovered&&(this._isHovered=!1)}},{key:"multiple",get:function(){return this._multiple},set:function(l){this._multiple=s(l)}},{key:"maxFileSize",get:function(){return this._maxFileSize},set:function(l){this._maxFileSize=function(l){return isNaN(parseFloat(l))||isNaN(Number(l))?null:Number(l)}(l)}},{key:"expandable",get:function(){return this._expandable},set:function(l){this._expandable=s(l)}},{key:"disableClick",get:function(){return this._disableClick},set:function(l){this._disableClick=s(l)}}]),l}(),h=function(n){l(i,n);var e=t(i);function i(l){var n;return u(this,i),(n=e.call(this,l)).defualtImgLoading="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiBzdHlsZT0ibWFyZ2luOiBhdXRvOyBiYWNrZ3JvdW5kOiByZ2IoMjQxLCAyNDIsIDI0Mykgbm9uZSByZXBlYXQgc2Nyb2xsIDAlIDAlOyBkaXNwbGF5OiBibG9jazsgc2hhcGUtcmVuZGVyaW5nOiBhdXRvOyIgd2lkdGg9IjIyNHB4IiBoZWlnaHQ9IjIyNHB4IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPgo8Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSIxNCIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2U9IiM4NWEyYjYiIHN0cm9rZS1kYXNoYXJyYXk9IjIxLjk5MTE0ODU3NTEyODU1MiAyMS45OTExNDg1NzUxMjg1NTIiIGZpbGw9Im5vbmUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCI+CiAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIGR1cj0iMS4xNjI3OTA2OTc2NzQ0MTg0cyIgcmVwZWF0Q291bnQ9ImluZGVmaW5pdGUiIGtleVRpbWVzPSIwOzEiIHZhbHVlcz0iMCA1MCA1MDszNjAgNTAgNTAiPjwvYW5pbWF0ZVRyYW5zZm9ybT4KPC9jaXJjbGU+CjxjaXJjbGUgY3g9IjUwIiBjeT0iNTAiIHI9IjEwIiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZT0iI2JiY2VkZCIgc3Ryb2tlLWRhc2hhcnJheT0iMTUuNzA3OTYzMjY3OTQ4OTY2IDE1LjcwNzk2MzI2Nzk0ODk2NiIgc3Ryb2tlLWRhc2hvZmZzZXQ9IjE1LjcwNzk2MzI2Nzk0ODk2NiIgZmlsbD0ibm9uZSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIj4KICA8YW5pbWF0ZVRyYW5zZm9ybSBhdHRyaWJ1dGVOYW1lPSJ0cmFuc2Zvcm0iIHR5cGU9InJvdGF0ZSIgZHVyPSIxLjE2Mjc5MDY5NzY3NDQxODRzIiByZXBlYXRDb3VudD0iaW5kZWZpbml0ZSIga2V5VGltZXM9IjA7MSIgdmFsdWVzPSIwIDUwIDUwOy0zNjAgNTAgNTAiPjwvYW5pbWF0ZVRyYW5zZm9ybT4KPC9jaXJjbGU+CjwhLS0gW2xkaW9dIGdlbmVyYXRlZCBieSBodHRwczovL2xvYWRpbmcuaW8vIC0tPjwvc3ZnPg==",n.imageSrc=n.sanitizer.bypassSecurityTrustUrl(n.defualtImgLoading),n}return r(i,[{key:"ngOnInit",value:function(){var l=this;this.readFile().then(function(n){return setTimeout(function(){return l.imageSrc=n})}).catch(function(l){return console.error(l)})}}]),i}(b),p=function l(){u(this,l)},g=function(n){l(i,n);var e=t(i);function i(l){return u(this,i),e.call(this,l)}return r(i,[{key:"ngOnInit",value:function(){this.file?(this.videoSrc=URL.createObjectURL(this.file),this.sanitizedVideoSrc=this.sanitizer.bypassSecurityTrustUrl(this.videoSrc)):console.error("No file to read. Please provide a file using the [file] Input property.")}},{key:"ngOnDestroy",value:function(){URL.revokeObjectURL(this.videoSrc)}}]),i}(b),v=function l(){u(this,l)}},uwSD:function(l,n,t){"use strict";t.d(n,"a",function(){return e});var e=function l(){u(this,l)}},zDob:function(l,n,t){"use strict";t.d(n,"a",function(){return d});var e=t("8Y7J"),i=t("5mnX"),a=t.n(i),o=t("h+Y6"),c=t.n(o),s=t("V99k"),d=function(){function l(n,t,i){u(this,l),this.data=n,this.dialogRef=t,this.fb=i,this.mode="create",this.source=s.w.PathSegment,this.onCreate=new e.o,this.formOptions={pathSegmentTypes:["Static","Alias"]},this.icClose=a.a,this.icLink=c.a}return r(l,[{key:"ngOnInit",value:function(){this.form=this.fb.group({name:null,type:"Alias"}),this.form.patchValue(this.data.alias||{})}},{key:"create",value:function(){this.onCreate.emit(this.form.value),this.dialogRef.close()}},{key:"isPathSegment",value:function(){return this.data.type===s.w.PathSegment}},{key:"getTitle",value:function(){return this.isPathSegment()?"Path Segment":"Alias"}}]),l}()}}])}();