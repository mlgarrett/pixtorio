var form = document.getElementById("form")
var submit_button = document.getElementById("generate")
var bp_string_field = document.getElementById("bp-string")
var uploadField = document.getElementById("source");
var preview_holder = document.getElementById("preview")
var scale_field = document.getElementById("scale")
var width_field = document.getElementById("width")
var height_field = document.getElementById("height")

scale_field.addEventListener("change", update_scales)

form.addEventListener('submit', function(event) {
    // prevent page from refreshing
    event.preventDefault()

    generate.disabled = true
    bp_string_field.value = "working..."
    preview_holder.innerHTML = "working..."

    // grab the data inside the form fields
    const formData = new FormData(form)
    fetch('/',
    {
        method: 'POST',
        body: formData,
    }).then(response => response.text()).then(message =>
    {
        message = JSON.parse(message)
        bp_string = message.bp_string
        preview = message.preview

        // decode the preview back to an image and place it in the preview box
        preview_holder.innerHTML = "<img src='data:image/png;base64,"+preview+"' style='max-width: 300px; max-height: 300px; height: auto;' alt='Rough Preview' />"

        // do something with the response
        outspan = document.getElementById("bp-string")
        outspan.value = bp_string
        generate.disabled = false
    })
})

function update_scales()
{
    if (uploadField.files && uploadField.files[0])
    {
        var reader = new FileReader();
        reader.readAsDataURL(uploadField.files[0])
        reader.onload = function(e)
        {
            var image = new Image()
            image.src = e.target.result;

            image.onload = function()
            {
                // get image dims
                image_width = this.width
                image_height = this.height
                width_field.innerHTML = "&nbsp;w: " + Math.round(scale_field.value*image_width) + "&nbsp;"
                height_field.innerHTML = "&nbsp;h: " + Math.round(scale_field.value*image_height)
            };
        };
    }
}

function copyString()
{
    var string_textbox = document.getElementById("bp-string")

    navigator.clipboard.writeText(string_textbox.value)
}

uploadField.onchange = function()
{
    // 2.5 megabytes limit
    if(this.files[0].size > 2621440)
    {
        alert("File is too large!\nPlease use a file that is < 2.5Mb.");
        this.value = "";
        return
    }

    update_scales()
}

$( "#sortable" ).sortable({
    placeholder: "placeholder",
    forcePlaceholderSize: true,
    helper: "helper",
    forceHelperSize: true,
    cursor: "move",
    axis: "y",
    revert: 250,
})
$( "#sortable" ).disableSelection()
