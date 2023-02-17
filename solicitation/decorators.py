from django.shortcuts import redirect


from django.contrib import messages
from help_pages.models import VisualizacaoBlog


def complete_tutorial(view_func):
    def wrapper_func(request, *args, **Kwargs):    
        if request.user.is_authenticated:
            userid = request.user.id
            viewconfirmation = VisualizacaoBlog.objects.filter(User_id=userid, Post_id__in=(1, 2, 5, 6)).count()                          
            passos = []
            if viewconfirmation < 4:
                passos = viewconfirmation                    
                messages.warning(
                request,
                f'Você deverá ler os tutoriais: '
                f'CONHECENDO O CHAMADO-DP PARTE 1, 2 ,3 e 4 '
                f'Antes de Começar a usar o sistema! '           
                )

                if passos > 0:
                    messages.success(
                        request,
                        f'Passo {passos} de 4'     
                    )                                              
                return redirect('help_pages:blog_tutoriais')                   
            else:                         
                return view_func(request, *args, **Kwargs)
        else:
            return redirect('accounts:login')
    return wrapper_func