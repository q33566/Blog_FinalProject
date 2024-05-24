var article = document.getElementById("recommandedArticle");
article.addEventListener("click", function () {
    document.getElementsByClassName("recommandedArticleList").hidden = false;
    document.getElementsByClassName("tagArticleList").hidden = true;
    console.log("recommandedArticle clicked");
});

var xhr = new XMLHttpRequest();