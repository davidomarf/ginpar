function updateVars(){
    let attrs = {{attrs}}
    for(let i = 0; i < attrs.length; i++){
        let el = document.getElementById(attrs[i].id)
        if (el){
            console.log(
                attrs[i].name, 
                document.getElementById(attrs[i].id).value)
        }
    }
}

updateVars()