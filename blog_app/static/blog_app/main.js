const soon_tags = document.querySelectorAll("a.soon");
let originalText = soon_tags.innerText; 


soon_tags.forEach((link)=>{

    link.addEventListener('mouseover',(e)=>{
        e.preventDefault();
        console.log(e.target.nextElementSibling);
        let pop = e.target.nextElementSibling;
        pop.classList.add('pop-up-visible');

})

    link.addEventListener('mouseleave',(e)=>{
        e.preventDefault();

        let pop = e.target.nextElementSibling;
        pop.classList.remove('pop-up-visible');
          
})

})



