async function buscarPais(nombre) {
      const input = document.getElementById('searchInput');
      const country = nombre || input.value.trim();
      if (!country) return alert('Escribe un nombre de país');

      const res = await fetch(`/busqueda?country=${country}`);
      if (!res.ok) return alert('País no encontrado');

      const data = await res.json();
      document.getElementById('flag').src = data.flag;
      document.getElementById('name').innerText = data.name;
      document.getElementById('capital').innerText = data.capital;
      document.getElementById('region').innerText = data.region;
      document.getElementById('population').innerText = data.population;
      document.getElementById('area').innerText = data.area;
      document.getElementById('languages').innerText = data.languages;
      document.getElementById('currencies').innerText = data.currencies;
      document.getElementById('infoContainer').style.display = 'block';
      document.getElementById('sugerencias').innerHTML = '';
    }

    async function mostrarSugerencias(event) {
      const valor = event.target.value.trim();
      const lista = document.getElementById('sugerencias');

      if (!valor) {
        lista.innerHTML = '';
        return;
      }

      const res = await fetch(`/autocompletado?q=${valor}`);
      const sugerencias = await res.json();

      lista.innerHTML = '';
      sugerencias.forEach(nombre => {
        const li = document.createElement('li');
        li.textContent = nombre;
        li.onclick = () => {
          document.getElementById('searchInput').value = nombre;
          buscarPais(nombre);
        };
        lista.appendChild(li);
      });
    }

    function detectarEnter(e) {
      if (e.key === 'Enter') buscarPais();
    }