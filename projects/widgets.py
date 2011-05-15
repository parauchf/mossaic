

class tokenizingInputWidget(forms.TextInput):
	def __init__(self, source, options={}, attrs={}):
		
		self.options = None
		self.attrs = {'autocomplete': 'off'}
		self.source = source
		if len(options) > 0:
			self.options = JSONEncoder().encode(options)

	def render_js(self,field_id):
		if isinstance(self.source, list):
			source = JSONEncoder().encode(self.source)
		elif isinstance(self.source, str):
			source = "'%s'" % escape(self.source)
		else:
			raise ValueError('source type is not valid')

		options = ''
		if self.options:
			options += ',%s' % self.options
		
		return u'$(\'#%s\').autocomplete(%s%s);' % (field_id, source, options)
		
	def render(self, name, value=None, attrs=None):
		final_attrs = self.build_attrs(attrs, name=name)
		if value:
			final_attrs['value'] = escape(smart_unicode(value))

		if not self.attrs.has_key('id'):
			final_attrs['id'] = 'id_%s' % name    

		return u'''<input type="text" %(attrs)s/>
		<script type="text/javascript"><!--//
		%(js)s//--></script>
		''' % {
			'attrs' : flatatt(final_attrs),
			'js' : self.render_js(final_attrs['id']),
        }