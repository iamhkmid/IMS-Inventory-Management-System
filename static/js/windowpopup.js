function popitup(url){
    newwindow=window.open(url,'New Window','height=600,width=1000');
    if (window.focus){newwindow.focus()}
    return false;
}