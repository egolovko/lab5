from student import Student


class Information:
	_instance = None

	def __init__(self):
		self._students = []

	@staticmethod
	def get_instance():
		if Information._instance is None:
			Information._instance = Information()

		return Information._instance

	def clear(self):
		self._students.clear()

	def load(self, npass, ngroup, fname, lname, patronymic, subject, score, total_score_100, total_score_5):
		try:
			student = self.find(npass)
		except ValueError:
			student = self.add(npass, ngroup)

		if student.ngroup != ngroup:
			raise ValueError

		student.load(fname, lname, patronymic, subject, score, total_score_100, total_score_5)

	def add(self, npass, ngroup) -> Student:
		new_student = Student(npass, ngroup)
		self._students.append(new_student)
		return new_student

	def find(self, npass) -> Student:
		index = self._students.index(Student(npass))
		student = self._students[index]
		return student

	def output(self, path, encoding):
		print(f"output {path}:", end=" ")
		print("OK")
		pass

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		if exc_type is not None:
			self.clear()

