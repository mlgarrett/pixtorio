var form = document.getElementById("form")
var submit_button = document.getElementById("generate")
var bp_string_field = document.getElementById("bp-string")
var uploadField = document.getElementById("source");
var preview_holder = document.getElementById("preview-holder")
var scale_field = document.getElementById("scale")
var width_field = document.getElementById("width")
var height_field = document.getElementById("height")
var outspan = document.getElementById("bp-string")
var copy_btn = document.getElementById("copy-btn")

form.addEventListener('submit', function(event) {
    // prevent page from refreshing
    event.preventDefault()

    generate.disabled = true
    copy_btn.disabled = true
    bp_string_field.value = "working..."
    preview_holder.innerHTML = "<div class='preview-loader' id='preview-loader'></div>"

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
        if (bp_string)
        {
            preview = message.preview

            // decode the preview back to an image and place it in the preview box
            preview_holder.innerHTML = "<img src='data:image/png;base64,"+preview+"' style='max-width: 300px; max-height: 300px; height: auto;' alt='Rough Preview' />"

            // do something with the response
            outspan.value = bp_string
        }
        else
        {
            outspan.value = "error! invalid file type provided."
            preview_holder.innerHTML = "error! invalid file type provided."
        }
        generate.disabled = false
        copy_btn.disabled = false
    })
})

function update_scales(dimensions)
{
        width_field.innerHTML = "&nbsp;w: " + Math.round(scale_field.value*dimensions[0]) + "&nbsp;"
        height_field.innerHTML = "&nbsp;h: " + Math.round(scale_field.value*dimensions[1])
}

function get_upload_dimensions(dimension_callback)
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
                // get the image dimensions and return if max pixels is exceeded
                if (this.width*this.height > 256**2)
                {
                    // alert("Resolution is too high! Please limit to 1MP (1024x1024).")
                    // do something about the dimensions here?
                    // compute a scaling factor with a max in one dimension
                    scale = Math.min(1, Math.min(256/this.width, 256/this.height))
                    // compute the new blueprint width and height
                    bp_width = Math.round(this.width*scale)
                    bp_height = Math.round(this.height*scale)

                    dimension_callback([bp_width, bp_height])
                }
                else
                {
                    dimension_callback([this.width, this.height])
                }
            }
        }
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
        alert("File is too large! Please use a file that is < 2.5MB.");
        this.value = "";
        return
    }
    else
    {
        get_upload_dimensions(function(dimensions)
        {
            update_scales(dimensions)
        })
    }
}

scale_field.onchange = function()
{
    get_upload_dimensions(function(dimensions)
    {
        update_scales(dimensions)
    })
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
