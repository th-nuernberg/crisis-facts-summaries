//Mock Script for the Website
function initAssignment(){
    let button = document.getElementById("calculate_button");
    button.addEventListener("click",make_a_summary)
}



async function make_a_summary(){
   if(document.getElementById("new_summary") != null){
    document.getElementById("new_summary").remove();
   }
    
   //ALERT currently no check if data is valid
   // TODO n-Gramm Als number Drop down
   let ngramms = document.getElementById("ngram").value;
   let timespan = document.getElementById("time").value;
   let weight = document.getElementById("weight").value;
   let max_length = document.getElementById("max_length").value;
   
   let summary_question = document.getElementById("text_area").value;

   let variables_for_summary = [{"ngrams": ngramms, "timespan": timespan, "weight":weight, "max_length": max_length, "question": summary_question}];
   let response_json;

   await fetch("http://127.0.0.1:5000/summarize", 
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
            // Strigify the payload into JSON:
            body:JSON.stringify(variables_for_summary)
        }).then( (response) =>{
            if(response.ok){
                //alert(response.json());
                return response.json();     //It returns a promise which resolves with the result of parsing the body text as JSON
            }else{
                alert("something is wrong" + response);
            }
        }).then(jsonResponse=>{

            o = JSON.stringify(jsonResponse);
            alert(o);
            //response_json = o;
            // Test Solution since Docker doesnt work well with windows
            // not made for Json at the moment
            response_json = jsonResponse
        }).catch((err) => console.error(err));

   let main_Container = document.getElementById("Summary")

   let new_summary = document.createElement("p");
   new_summary.setAttribute('id', "new_summary");
   
   new_summary.setAttribute('align', "left");

   new_summary.innerHTML = response_json;


   main_Container.append(new_summary);
   
}