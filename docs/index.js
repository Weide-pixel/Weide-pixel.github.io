const p = document.querySelector("#college_content");
const button = document.querySelector("#show_college");

button.addEventListener("click", readMore);

function readMore() 
{
    if(p.className == "college_click")          // 顯示文字
    {
        p.className = "college_content";
        button.innerHTML = "大學時期 &gt;";
    } 
    else        // 隱藏起文字
    {
        p.className = "college_click";
        button.innerHTML = "大學時期 &lt;";
    }
}