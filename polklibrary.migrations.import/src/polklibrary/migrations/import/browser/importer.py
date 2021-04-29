
from plone import api
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer
from plone.uuid.interfaces import ATTRIBUTE_NAME
from Products.Five import BrowserView
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
from plone.namedfile.file import NamedBlobFile,NamedBlobImage
import json, logging, time, requests, base64, io

logger = logging.getLogger("Plone")


class Importer(BrowserView):

    output = ''

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        self.output = 'IMPORTER INFORMATION --\n'
        url = self.request.form.get('url','')
        
        if url:
            response = requests.get(url)
            data = json.loads(response.text)
            
            self.create_content(data)

            
        return self.output


    def create_content(self, data):
        with api.env.adopt_roles(roles=['Manager']):
            item = createContentInContainer(self.context, data['portal_type'], id=data['getId'], title=data['title'])
            setattr(item, '_plone.uuid', data['_plone.uuid'])
            
            
            for k,v in data.items():
                key = k
                val = v
                
                if ':JSON' in key:
                    key = key.replace(':JSON', '')
                    setattr(item, key, self.from_base64(val))
                    
                elif ':IMAGE' in key:
                    key = key.replace(':IMAGE', '')
                    blob_data = NamedBlobImage(self.from_base64(val), filename=data['filename'])
                    setattr(item, key, blob_data)
                    
                elif ':FILE' in key:
                    key = key.replace(':FILE', '')
                    blob_data = NamedBlobFile(self.from_base64(val), filename=data['filename'])
                    setattr(item, key, blob_data)
                    
                elif 'subjects' in key:
                    item.setSubject(val)
                    
                elif 'review_state' in key:
                    workflowTool = getToolByName(item, "portal_workflow")
                    try:
                        state = ""
                        if data['review_state'] == 'published':
                            state = "publish"
                        elif data['review_state'] == 'private':
                            state = "retract"
                        if state:
                            workflowTool.doActionFor(item, "publish")
                    except Exception:
                        print("Could not change review_state")
                        
                elif any(x in key for x in ['filename','_plone.uuid','getId']): # SKIP
                    pass
                
                elif hasattr(item, key):
                    setattr(item, key, val)
                    
            item.reindexObject()
            self.output += "    imported: " + str(item.title) + " | " + str(item.getId()) + " | " + str(item.UID()) + "\n"



    def from_base64(self, data):
        return base64.b64decode(data)

    @property
    def portal(self):
        return api.portal.get()