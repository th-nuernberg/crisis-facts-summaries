//Mock Script for the Website
function initAssignment(){
    let button = document.getElementById("calculate_button");
    button.addEventListener("click",make_a_summary)
}



function make_a_summary(){
   if(document.getElementById("new_summary") != null){
    document.getElementById("new_summary").remove();
   }
    
    //ALERT currently no check if data is valid
   let ngramms = document.getElementById("ngram").value;
   let timespan = document.getElementById("time").value;
   let weight = document.getElementById("weight").value;
   let max_length = document.getElementById("max_length").value;
   
   let summary_question = document.getElementById("text_area").value

   let main_Container = document.getElementById("Summary")

   let new_summary = document.createElement("p");
   new_summary.setAttribute('id', "new_summary");
   
   new_summary.setAttribute('align', "left");

   new_summary.innerHTML =`A new Summary with ${ngramms} word-gramms, over the timespan of hour ${timespan}, with the weight of ${weight} and the maximum length of ${max_length} words.`;


   main_Container.append(new_summary);
   
}