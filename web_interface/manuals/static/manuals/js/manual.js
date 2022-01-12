
var manual_ = null;

function get_paragraph_signature(section, paragraph)
{
    return section + "-" + paragraph;
}

function get_sentence_signature(section, paragraph, sentence)
{
    return get_paragraph_signature(section, paragraph) + "-" + sentence;
}


function create_annotation_view(annotation)
{
    if (annotation.type == 'Ontology')
        return new OntologyView(annotation);
    else 
        return new StatementView(annotation);
}


class Sentence
{
    constructor(section, paragraph, sentence, url) {
        this.section = section;
        this.paragraph = paragraph;
        this.sentence = sentence;
        this.url = url;
        this.annotations = [];
        this.loaded = false;
    }

    get_id() {
        return get_sentence_signature(this.section, this.paragraph, this.sentence);
    }

    get_parent_id() {
        return get_paragraph_signature(this.section, this.paragraph);
    }
}

class SentenceView
{
    constructor(sentence) {
        this.sentence = sentence;
        this.visible = false;
        this.annotation_views = [];
    }

    get_div() {
        var id = "sentence-" + this.sentence.get_id();
        return document.getElementById(id);
    }    

    get_parent_div() {
        var id = "paragraph-" + this.sentence.get_parent_id();
        return document.getElementById(id);
    }    

    get_annotations_div() {
        var id = "annotations-" + this.sentence.get_id();
        return document.getElementById(id);
    }    

    toggle() {
        if (this.visible)
            this.hide();
        else
            this.show();
    }
    
    show() {
        this.visible = true;
        $(this.get_annotations_div()).show();
        $(this.get_div()).addClass('manual-border-color-' + this.sentence.sentence);
    }

    hide() {
        this.visible = false;
        $(this.get_annotations_div()).hide();
        $(this.get_div()).removeClass('manual-border-color-' + this.sentence.sentence);
    }
    
    build() {
        var root = $('<div>', {
            'class': 'manual-sentence-annotations manual-border-color-' + this.sentence.sentence,
            'id': "annotations-" + this.sentence.get_id()
        });
        this.createSentenceSignatureView().appendTo(root);
        this.insertAnnotations(root);
        return root;
    }

    createSentenceSignatureView() {
        return $('<div>', {
            'class':  'manual-sentence-signature',
            'text':  this.createSentenceSignature(),
        });
    }
    
    createSentenceSignature() {
        return ("§" + this.sentence.section
                + " ¶" + this.sentence.paragraph
                + " S" + this.sentence.sentence);
    }
    
    insertAnnotations(root) {
        var annotations = this.sentence.annotations;
        if (annotations && annotations.length) {
            for (let i = 0; i < annotations.length; i++) {
                var view = create_annotation_view(annotations[i]);
                this.annotation_views.push(view);
                view.div.appendTo(root);
            }
        }
    }
}

class StatementView
{
    constructor(annotation) {
        this.annotation = annotation;
        this.div = null;
        this.build();
    }
    
    build() {
        var card = $('<div>', {
            'class': 'card manual-sentence-annotation mb-2'
        });
        var header = $('<div>', {
            'class': 'card-header manual-annotation-type pt-0 pb-0 pl-2',
            'text': this.annotation.type });
        header.appendTo(card);
        var body = $('<div>', {
            'class': 'card-body pt-1 pb-1 pl-2'
        });
        body.appendTo(card);
        var subject = $('<div>', {
            'class': 'annotation-subject',
            'text': this.annotation.content.subject + ": "
        });
        subject.appendTo(body);
        var text = $('<div>', {
            'class': 'annotation-text',
            'text': this.annotation.content.text
        });
        text.appendTo(body);
        var footer = $('<div>', {
            'class': 'card-footer manual-annotation-evaluation pt-0 pb-0 pl-2',
            'text': 'Agree: 0, Disagree: 0, References: 0, Datasets: 0' });
        footer.appendTo(card);
        this.div = card;
        return card;
    }
}

class OntologyView
{
    constructor(annotation) {
        this.annotation = annotation;
        this.div = null;
        this.build();
    }
    
    build() {
        var card = $('<div>', {
            'class': 'card manual-sentence-annotation mb-2'
        });
        var header = $('<div>', {
            'class': 'card-header manual-annotation-type pt-0 pb-0 pl-2',
            'text': this.annotation.type });
        header.appendTo(card);
        var body = $('<div>', {
            'class': 'card-body pt-1 pb-1 pl-2'
        });
        body.appendTo(card);
        var subject = $('<div>', {
            'class': 'ontology-name',
            'text': this.annotation.content.names.join(', ') + ": "
        });
        subject.appendTo(body);
        var text = $('<div>', {
            'class': 'ontology-description',
            'text': this.annotation.content.description
        });
        text.appendTo(body);

        var tree = $('<div>', {
            'class': 'ontology-children',
        });
        tree.appendTo(body);
        
        var ul = $('<ul>', { 'class': 'ontology-children' }).appendTo(tree);
        
        for (let i = 0; i <  this.annotation.content.children.length; i++) {
            var child = this.annotation.content.children[i];
            var li = $('<li>', { 'class': 'xxx' }).appendTo(ul);
            $('<span>', { 'class': 'ontology-child-name', 'text': child.names.join(', ') }).appendTo(li);
            if (child.description) {
                $('<span>', { 'class': 'ontology-child-description', 'text': child.description }).appendTo(li);
            }
        }
        
        var footer = $('<div>', {
            'class': 'card-footer manual-annotation-evaluation pt-0 pb-0 pl-2',
            'text': 'Agree: 0, Disagree: 0, References: 0, Datasets: 0' });
        footer.appendTo(card);
        this.div = card;
        return card;
    }
}

class Manual
{
    constructor(label) {
        this.label = label;
        this.annotations = {};
        this.sentence_views = {};
        this.annotation_views = [];
    }

    showAnnotations(sentence) {
        var div = sentence.get_div();
        $(div).show();
        $('#'+sentence.signature).css('background-color', 'yellow');
        sentence.visible = true;
    }

    hideAnnotations(pid, sid) {
        var div = sentence.get_div();
        $(div).hide();
        $('#'+sid).css('background-color', '');
        sentence.visible = false;
    }

    toggleAnnotations(section, paragraph, sentence, url) {
        var id = get_sentence_signature(section, paragraph, sentence);
        var view = this.sentence_views[id];
        
        if (!view) {
            sentence = new Sentence(section, paragraph, sentence, url);
            this.loadAnnotations(sentence);
        } else {
            view.toggle();
        }
    }

    loadAnnotations(sentence) {
        var self = this;
        $.getJSON(sentence.url, function(data) {
            self.importAnnotations(sentence, JSON.parse(data));
        });
    }

    importAnnotations(sentence, data) {
        //console.log("importAnnotations: annotations=" + JSON.stringify(data));
        sentence.annotations = data;
        sentence.loaded = true;
        var view = new SentenceView(sentence);
        this.sentence_views[sentence.get_id()] = view;
        view.build().appendTo(view.get_parent_div());
        view.show();
    }

    loadAllAnnotations(url) {
        var self = this;
        $.getJSON(url, function(data) {
            self.importAllAnnotations(JSON.parse(data));
        });
    }

    importAllAnnotations(annotations) {
        var root = document.getElementById('manual-annotation-list');
        if (annotations && annotations.length) {
            for (let i = 0; i < annotations.length; i++) {

                if (annotations[i].type == 'Ontology') {
                    console.log(annotations[i].content);
                }
                var view = create_annotation_view(annotations[i]);
                this.annotation_views.push(view);
                view.div.appendTo(root);
            }
        }
    }
}

function initManual(label)
{
    manual_ = new Manual(label);
}

function toggleAnnotations(section, paragraph, sentence, url)
{
    manual_.toggleAnnotations(section, paragraph, sentence, url);
}

function loadAllAnnotation(url)
{
    console.log("Load " + url);
    manual_.loadAllAnnotations(url);
}


