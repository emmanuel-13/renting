;(function($){
    $(document).ready(function(){
        $(document).tooltip({
            content: function () {
                return $(this).attr('title');
            }
        });

        $(".btn-copy").click(function(){
            var text = $(this).attr("copy-value");
            navigator.clipboard.writeText(text);
        });
    });
})(jQuery);