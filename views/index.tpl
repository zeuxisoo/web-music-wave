%include header title = title
<div class="box">
	<form action="/generate" method="post" enctype="multipart/form-data">
	Music: 
	<input type="file" name="music" id="music" />
	<input type="submit" name="commit" id="commit" />
	</form>
</div>
%include footer title = title