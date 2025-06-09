from typing import Optional

def insertsort(array, field: str):
	for i in range(1, len(array)):
		element = array[i]
		j = i
		while j > 0 and element.compare(array[j - 1], field) > 0:
			array[j] = array[j - 1]
			j -= 1
		array[j] = element

def merge(array, field: str, frm: int, pivot: int, to: int, len1: int, len2: int):
	if len1 == 0 or len2 == 0:
		return
	if len1 + len2 == 2:
		if array[pivot].compare(array[frm], field) > 0:
			array[pivot], array[frm] = array[frm], array[pivot]
		return
	if len1 > len2:
		len11 = int(len1 / 2)
		firstcut, secondcut, length = frm + len11, pivot, to-pivot
		while length > 0:
			half = int(length / 2)
			mid = secondcut+half
			if array[mid].compare(array[firstcut], field) > 0:
				secondcut, length = mid+1, length-half-1
			else:
				length = half
		len22 = secondcut - pivot
	else:
		len22 = int(len2 / 2)
		firstcut, secondcut, length = frm, pivot + len22, pivot-frm
		while length > 0:
			half = int(length / 2)
			mid = firstcut+half
			if array[secondcut].compare(array[mid], field) > 0:
				length = half
			else:
				firstcut, length = mid+1, length-half-1
		len11 = firstcut - frm
	if firstcut!=pivot and pivot!=secondcut:
		n, m = secondcut-firstcut, pivot-firstcut
		while m != 0: n, m = m, n%m
		while n != 0:
			n -= 1
			p1, p2 = firstcut+n, n+pivot
			val, shift = array[p1], p2-p1
			while p2 != firstcut+n:
				array[p1], p1 = array[p2], p2
				if secondcut-p2>shift:
					p2 += shift
				else:
					p2 = pivot-secondcut+p2
			array[p1] = val
	newmid = firstcut + len22
	merge(array, field, frm, firstcut, newmid, len11, len22)
	merge(array, field, newmid, secondcut, to, len1-len11, len2-len22)

def mergesort(array, field: str, frm: int = 0, to:Optional[int] = None):
	if to is None:
		to = len(array)
	if to - frm < 2:
		return
	middle = int((frm + to) / 2)
	mergesort(array, field, frm, middle)
	mergesort(array, field, middle, to)
	merge(array, field, frm, middle, to, middle - frm, to - middle)
