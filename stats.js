/* Statistics (Microsoft Clarity): loaded only for visitors who accepted the cookie banner. */
(function(){
  var ID="zfpgvzgbez"; // Clarity project ID, from clarity.microsoft.com > Settings > Overview
  window.evStats=function(on){
    if(!ID)return;
    if(on===false){if(window.clarity)window.clarity("consent",false);return;}
    if(!window.clarity){(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script",ID);}
    window.clarity("consent");
  };
  try{if(localStorage.getItem("ev-stats")==="yes")window.evStats(true);}catch(e){}
})();
