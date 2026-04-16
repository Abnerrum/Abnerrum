const botoesStatus = document.querySelectorAll('.toggle-status');

botoesStatus.forEach((botao) => {
  botao.addEventListener('click', async () => {
    const tarefaId = botao.dataset.id;

    try {
      const resposta = await fetch(`/tarefas/${tarefaId}/status`, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      if (!resposta.ok) {
        throw new Error('Falha ao atualizar status');
      }

      window.location.reload();
    } catch (erro) {
      alert('Não foi possível atualizar a tarefa agora.');
      console.error(erro);
    }
  });
});
