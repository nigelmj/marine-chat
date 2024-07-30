class Typing {
  constructor(opts) {
    this.version = "1.1";
    this.source = opts.source;
    this.output = opts.output;
    this.delay = opts.delay || 120;
    this.chain = {
      parent: null,
      dom: this.output,
      val: [],
    };
    this.scrollThreshold = 0;
  }

  toArray(eles) {
    return Array.from(eles);
  }

  init() {
    this.chain.val = this.convert(this.source, this.chain.val);
  }

  convert(dom, arr) {
    const children = this.toArray(dom.childNodes);

    children.forEach((node) => {
      if (node.nodeType === 3) {
        arr = arr.concat(node.nodeValue.split(""));
      } else if (node.nodeType === 1) {
        const val = this.convert(node, []);
        arr.push({
          dom: node,
          val: val,
        });
      }
    });

    return arr;
  }

  print(dom, val, callback) {
    setTimeout(() => {
      dom.appendChild(document.createTextNode(val));
      callback();
      this.checkScroll();
    }, this.delay);
  }

  checkScroll() {
    const outputDiv = this.output;
    const contentDiv = document.querySelector(".content");

    const outputRect = outputDiv.getBoundingClientRect();
    const contentRect = contentDiv.getBoundingClientRect();

    const scrollThreshold = this.scrollThreshold || 0;

    if (outputRect.bottom > contentRect.bottom + scrollThreshold) {
      this.scrollToBottom();
    }
  }

  play(ele) {
    if (!ele) return;
    if (!ele.val.length && ele.parent) this.play(ele.parent);
    if (!ele.val.length) return;

    const curr = ele.val.shift();

    if (typeof curr === "string") {
      this.print(ele.dom, curr, () => {
        if (ele.val.length) {
          this.play(ele);
        } else if (ele.parent) {
          this.play(ele.parent);
        }
      });
    } else {
      const dom = document.createElement(curr.dom.nodeName);
      const attrs = this.toArray(curr.dom.attributes);
      attrs.forEach((attr) => {
        dom.setAttribute(attr.name, attr.value);
      });
      ele.dom.appendChild(dom);
      curr.parent = ele;
      curr.dom = dom;
      this.play(curr.val.length ? curr : curr.parent);
    }
  }

  start() {
    this.init();
    this.play(this.chain);
  }

  scrollToBottom() {
    const contentDiv = document.querySelector(".content");
    contentDiv.scroll({
      top: contentDiv.scrollHeight,
      behavior: "smooth",
    });
  }
}
