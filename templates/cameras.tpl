<h2>Camaras disponibles</h2>
<div class="centrado">
	<ul>
		#for $camera in $cameras:
			<li><a href="/view/$camera.id">$camera.device_path</a></li>
		#end for
	</ul>
</div>
