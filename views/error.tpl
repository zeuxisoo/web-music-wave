%include header title = title
<div class="box">
	<div class="error">
		%if status == "no-upload-file":
			Please submit upload file
		%elif status == "invalid-upload-file":
			Invalid file! (support format: .wav, .aiff, .au, .ogg, .flac, .mp3)
		%elif status == "no-preview-file":
			Not found preview file
		%else:
			No action
		%end
	</div>
	<div class="back">
		&laquo; <a href="/">Back!</a>
	</div>
</div>
%include footer title = title