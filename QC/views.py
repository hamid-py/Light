from django.shortcuts import render

from .forms import QcScoreForm


def qc_score(request):
    if request.method == 'POST':
        pass
    form = QcScoreForm()
    return render(request, 'QC/score.html', {'form': form})
