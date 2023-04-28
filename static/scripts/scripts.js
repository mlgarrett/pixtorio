            var form = document.getElementById("form")
            var submit_button = document.getElementById("generate")
            var bp_string_field = document.getElementById("bp-string")
            var uploadField = document.getElementById("source");

            form.addEventListener('submit', function(event) {
                // prevent page from refreshing
                event.preventDefault()

                generate.disabled = true
                bp_string_field.value = "working..."

                // grab the data inside the form fields
                const formData = new FormData(form)
                fetch('/',
                {
                    method: 'POST',
                    body: formData,
                }).then(response => response.text()).then((message) =>
                {
                    // do something with the response
                    outspan = document.getElementById("bp-string")
                    outspan.value = message
                    generate.disabled = false
                })
            })

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
                }
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
