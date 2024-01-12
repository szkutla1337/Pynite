const menuButton = document.querySelector("#menuBtn");

menuButton.addEventListener("click", function(){
  const currentState = menuButton.getAttribute("aria-expanded");
  const menuButtonsDiv = document.querySelector("#menuButtonsDiv");
  
  if (currentState == "false"){
    menuButton.setAttribute("aria-expanded", "true");
    console.log("test");
    menuButton.style.marginTop = "4px";
    menuButtonsDiv.style.top = "68px";
  } else{
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.style.marginTop = "0px";
    menuButtonsDiv.style.top = "-200px";
  }
})



let buttonWidget = document.querySelector("#buttonWidget");
let buttonDesc = document.querySelector("#buttonDesc");
let buttonSpanPlus = document.querySelector("#buttonSpanPlus");
let buttonWidgetDiv = document.querySelector("#buttonWidgetDiv");
let buttonDescShown = false;

buttonWidget.addEventListener("click", function(){
  if (!buttonDescShown){
    buttonDescShown = true;
    buttonDesc.style.display = "flex";
    buttonSpanPlus.innerHTML = "-";
    buttonWidgetDiv.style.paddingBottom = "20px";
  } else{
    buttonDescShown = false;
    buttonDesc.style.display = "none";
    buttonSpanPlus.innerHTML = "+";
    buttonWidgetDiv.style.paddingBottom = "0px";
  }
});

let labelWidget = document.querySelector("#labelWidget");
let labelDesc = document.querySelector("#labelDesc");
let labelSpanPlus = document.querySelector("#labelSpanPlus");
let labelWidgetDiv = document.querySelector("#labelWidgetDiv");
let labelDescShown = false;

labelWidget.addEventListener("click", function(){
  if (!labelDescShown){
    labelDescShown = true;
    labelDesc.style.display = "flex";
    labelSpanPlus.innerHTML = "-";
    labelWidgetDiv.style.paddingBottom = "20px";
  } else{
    labelDescShown = false;
    labelDesc.style.display = "none";
    labelSpanPlus.innerHTML = "+";
    labelWidgetDiv.style.paddingBottom = "0px";
  }
});

let rectangleWidget = document.querySelector("#rectangleWidget");
let rectangleDesc = document.querySelector("#rectangleDesc");
let rectangleSpanPlus = document.querySelector("#rectangleSpanPlus");
let rectangleWidgetDiv = document.querySelector("#rectangleWidgetDiv");
let rectangleDescShown = false;

rectangleWidget.addEventListener("click", function(){
  if (!rectangleDescShown){
    rectangleDescShown = true;
    rectangleDesc.style.display = "flex";
    rectangleSpanPlus.innerHTML = "-";
    rectangleWidgetDiv.style.paddingBottom = "20px";
  } else{
    rectangleDescShown = false;
    rectangleDesc.style.display = "none";
    rectangleSpanPlus.innerHTML = "+";
    rectangleWidgetDiv.style.paddingBottom = "0px";
  }
});

let textBoxWidget = document.querySelector("#textBoxWidget");
let textBoxDesc = document.querySelector("#textBoxDesc");
let textBoxSpanPlus = document.querySelector("#textBoxSpanPlus");
let textBoxWidgetDiv = document.querySelector("#textBoxWidgetDiv");
let textBoxDescShown = false;

textBoxWidget.addEventListener("click", function(){
  if (!textBoxDescShown){
    textBoxDescShown = true;
    textBoxDesc.style.display = "flex";
    textBoxSpanPlus.innerHTML = "-";
    textBoxWidgetDiv.style.paddingBottom = "20px";
  } else{
    textBoxDescShown = false;
    textBoxDesc.style.display = "none";
    textBoxSpanPlus.innerHTML = "+";
    textBoxWidgetDiv.style.paddingBottom = "0px";
  }
});

let imageWidget = document.querySelector("#imageWidget");
let imageDesc = document.querySelector("#imageDesc");
let imageSpanPlus = document.querySelector("#imageSpanPlus");
let imageWidgetDiv = document.querySelector("#imageWidgetDiv");
let imageDescShown = false;

imageWidget.addEventListener("click", function(){
  if (!imageDescShown){
    imageDescShown = true;
    imageDesc.style.display = "flex";
    imageSpanPlus.innerHTML = "-";
    imageWidgetDiv.style.paddingBottom = "20px";
  } else{
    imageDescShown = false;
    imageDesc.style.display = "none";
    imageSpanPlus.innerHTML = "+";
    imageWidgetDiv.style.paddingBottom = "0px";
  }
});

let imageButtonWidget = document.querySelector("#imageButtonWidget");
let imageButtonDesc = document.querySelector("#imageButtonDesc");
let imageButtonSpanPlus = document.querySelector("#imageButtonSpanPlus");
let imageButtonWidgetDiv = document.querySelector("#imageButtonWidgetDiv");
let imageButtonDescShown = false;

imageButtonWidget.addEventListener("click", function(){
  if (!imageButtonDescShown){
    imageButtonDescShown = true;
    imageButtonDesc.style.display = "flex";
    imageButtonSpanPlus.innerHTML = "-";
    imageButtonWidgetDiv.style.paddingBottom = "20px";
  } else{
    imageButtonDescShown = false;
    imageButtonDesc.style.display = "none";
    imageButtonSpanPlus.innerHTML = "+";
    imageButtonWidgetDiv.style.paddingBottom = "0px";
  }
});

let sliderWidget = document.querySelector("#sliderWidget");
let sliderDesc = document.querySelector("#sliderDesc");
let sliderSpanPlus = document.querySelector("#sliderSpanPlus");
let sliderWidgetDiv = document.querySelector("#sliderWidgetDiv");
let sliderDescShown = false;

sliderWidget.addEventListener("click", function(){
  if (!sliderDescShown){
    sliderDescShown = true;
    sliderDesc.style.display = "flex";
    sliderSpanPlus.innerHTML = "-";
    sliderWidgetDiv.style.paddingBottom = "20px";
  } else{
    sliderDescShown = false;
    sliderDesc.style.display = "none";
    sliderSpanPlus.innerHTML = "+";
    sliderWidgetDiv.style.paddingBottom = "0px";
  }
});

let switchWidget = document.querySelector("#switchWidget");
let switchDesc = document.querySelector("#switchDesc");
let switchSpanPlus = document.querySelector("#switchSpanPlus");
let switchWidgetDiv = document.querySelector("#switchWidgetDiv");
let switchDescShown = false;

switchWidget.addEventListener("click", function(){
  if (!switchDescShown){
    switchDescShown = true;
    switchDesc.style.display = "flex";
    switchSpanPlus.innerHTML = "-";
    switchWidgetDiv.style.paddingBottom = "20px";
  } else{
    switchDescShown = false;
    switchDesc.style.display = "none";
    switchSpanPlus.innerHTML = "+";
    switchWidgetDiv.style.paddingBottom = "0px";
  }
});

let circleWidget = document.querySelector("#circleWidget");
let circleDesc = document.querySelector("#circleDesc");
let circleSpanPlus = document.querySelector("#circleSpanPlus");
let circleWidgetDiv = document.querySelector("#circleWidgetDiv");
let circleDescShown = false;

circleWidget.addEventListener("click", function(){
  if (!circleDescShown){
    circleDescShown = true;
    circleDesc.style.display = "flex";
    circleSpanPlus.innerHTML = "-";
    circleWidgetDiv.style.paddingBottom = "20px";
  } else{
    circleDescShown = false;
    circleDesc.style.display = "none";
    circleSpanPlus.innerHTML = "+";
    circleWidgetDiv.style.paddingBottom = "0px";
  }
});

let colorPickerWidget = document.querySelector("#colorPickerWidget");
let colorPickerDesc = document.querySelector("#colorPickerDesc");
let colorPickerSpanPlus = document.querySelector("#colorPickerSpanPlus");
let colorPickerWidgetDiv = document.querySelector("#colorPickerWidgetDiv");
let colorPickerDescShown = false;

colorPickerWidget.addEventListener("click", function(){
  if (!colorPickerDescShown){
    colorPickerDescShown = true;
    colorPickerDesc.style.display = "flex";
    colorPickerSpanPlus.innerHTML = "-";
    colorPickerWidgetDiv.style.paddingBottom = "20px";
  } else{
    colorPickerDescShown = false;
    colorPickerDesc.style.display = "none";
    colorPickerSpanPlus.innerHTML = "+";
    colorPickerWidgetDiv.style.paddingBottom = "0px";
  }
});

let surfaceWidget = document.querySelector("#surfaceWidget");
let surfaceDesc = document.querySelector("#surfaceDesc");
let surfaceSpanPlus = document.querySelector("#surfaceSpanPlus");
let surfaceWidgetDiv = document.querySelector("#surfaceWidgetDiv");
let surfaceDescShown = false;

surfaceWidget.addEventListener("click", function(){
  if (!surfaceDescShown){
    surfaceDescShown = true;
    surfaceDesc.style.display = "flex";
    surfaceSpanPlus.innerHTML = "-";
    surfaceWidgetDiv.style.paddingBottom = "20px";
  } else{
    surfaceDescShown = false;
    surfaceDesc.style.display = "none";
    surfaceSpanPlus.innerHTML = "+";
    surfaceWidgetDiv.style.paddingBottom = "0px";
  }
});

let animationWidget = document.querySelector("#animationWidget");
let animationDesc = document.querySelector("#animationDesc");
let animationSpanPlus = document.querySelector("#animationSpanPlus");
let animationWidgetDiv = document.querySelector("#animationWidgetDiv");
let animationDescShown = false;

animationWidget.addEventListener("click", function(){
  if (!animationDescShown){
    animationDescShown = true;
    animationDesc.style.display = "flex";
    animationSpanPlus.innerHTML = "-";
    animationWidgetDiv.style.paddingBottom = "20px";
  } else{
    animationDescShown = false;
    animationDesc.style.display = "none";
    animationSpanPlus.innerHTML = "+";
    animationWidgetDiv.style.paddingBottom = "0px";
  }
});

let progressBarWidget = document.querySelector("#progressBarWidget");
let progressBarDesc = document.querySelector("#progressBarDesc");
let progressBarSpanPlus = document.querySelector("#progressBarSpanPlus");
let progressBarWidgetDiv = document.querySelector("#progressBarWidgetDiv");
let progressBarDescShown = false;

progressBarWidget.addEventListener("click", function(){
  if (!progressBarDescShown){
    progressBarDescShown = true;
    progressBarDesc.style.display = "flex";
    progressBarSpanPlus.innerHTML = "-";
    progressBarWidgetDiv.style.paddingBottom = "20px";
  } else{
    progressBarDescShown = false;
    progressBarDesc.style.display = "none";
    progressBarSpanPlus.innerHTML = "+";
    progressBarWidgetDiv.style.paddingBottom = "0px";
  }
});

let checkBoxWidget = document.querySelector("#checkBoxWidget");
let checkBoxDesc = document.querySelector("#checkBoxDesc");
let checkBoxSpanPlus = document.querySelector("#checkBoxSpanPlus");
let checkBoxWidgetDiv = document.querySelector("#checkBoxWidgetDiv");
let checkBoxDescShown = false;

checkBoxWidget.addEventListener("click", function(){
  if (!checkBoxDescShown){
    checkBoxDescShown = true;
    checkBoxDesc.style.display = "flex";
    checkBoxSpanPlus.innerHTML = "-";
    checkBoxWidgetDiv.style.paddingBottom = "20px";
  } else{
    checkBoxDescShown = false;
    checkBoxDesc.style.display = "none";
    checkBoxSpanPlus.innerHTML = "+";
    checkBoxWidgetDiv.style.paddingBottom = "0px";
  }
});