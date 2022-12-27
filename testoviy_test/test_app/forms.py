from django.forms import ModelForm
from django.core.exceptions import ValidationError


class QuestionForm(ModelForm):

    def clean(self):
        data = self.data
        total_questions = data["questions-TOTAL_FORMS"]
        errors = []
        for i in range(int(total_questions)):
            total_answers = int(data[f'questions-{i}-answers-TOTAL_FORMS'])
            total_is_correct = 0

            for x in range(total_answers):
                if f"questions-{i}-answers-{x}-DELETE" in data.keys():
                    total_answers -= 1
                    continue

                elif f"questions-{i}-answers-{x}-is_correct" in data.keys():
                    total_is_correct += 1

            if total_answers == total_is_correct:
                errors.append(f"Выбраны все правильные ответы в вопросе {data[f'questions-{i}-text']}")
            elif total_is_correct == 0:
                errors.append(f"Нет правильного ответа в вопросе {data[f'questions-{i}-text']}")
        if errors:
            raise ValidationError(errors)