from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
from djangoklang.serveconll import serveconll

def index(request):
	return HttpResponse("Hello, world. You're at the serveconll index.")


@api_view(['GET', 'POST', 'OPTIONS'])
def conll(request):
	"""
	List all code snippets, or create a new snippet.
	"""
	if request.method == 'GET':
		# snippets = Snippet.objects.all()
		# serializer = SnippetSerializer(snippets, many=True)
		#
		# queryset = Group.objects.all()
		# serializer_class = GroupSerializer
		# return Response(serializer.data) request.query_params['qsdf']
		print(123123, request.query_params, request.user)
		# print(serveconll.allconlls())
		response = Response(
			{'hello': str(request.user), 'conlls': serveconll.allconlls()})
		# response.headers.add('Access-Control-Allow-Origin', '*')
		return response

	elif request.method == 'POST':
		# return Response({'nihao':'world'}) request.data["qsdf"],
		# print(456456,request, request.user, request.data)
		name = request.data.get('name', '')
		
		if name:
			r = serveconll.getconll(name)
			# print(5555,r)
			return Response({'conll': r})
		
		else:
			return Response({'hey': 'you!'}, status=status.HTTP_400_BAD_REQUEST)
		# serializer = SnippetSerializer(data=request.data)
		# if serializer.is_valid():
		#	 serializer.save()
		#	 return Response(serializer.data, status=status.HTTP_201_CREATED)
		# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

